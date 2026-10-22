<#
.SYNOPSIS
  Deletes the demo records for one or more claim IDs so the claims can be run again.

.DESCRIPTION
  Uses the Dataverse Web API with an Azure CLI access token. Deletes child records first:
  Item Valuations, Calculation Runs, Inventory Items, Approvals, Case Issues and Command Ledger
  entries, then the Valuation Case. Records are matched by Claim ID, or by a name that starts with
  the claim ID (the naming convention used by the CAT Contents Intake workflow).

  Run 'az login' first with an account that can delete these records.

.EXAMPLE
  ./Reset-DemoClaim.ps1 -OrgUrl https://zavacatdemo.crm.dynamics.com -ClaimId ZAV-1042,ZAV-1043 -WhatIf

.EXAMPLE
  ./Reset-DemoClaim.ps1 -OrgUrl https://zavacatdemo.crm.dynamics.com -ClaimId ZAV-1042,ZAV-1043
#>
[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)][string]$OrgUrl,
    [Parameter(Mandatory)][string[]]$ClaimId
)

$ErrorActionPreference = 'Stop'
$OrgUrl = $OrgUrl.TrimEnd('/')
$token = az account get-access-token --resource $OrgUrl --query accessToken -o tsv
if (-not $token) { throw "Couldn't get an access token. Run 'az login' and try again." }

$headers = @{
    Authorization      = "Bearer $token"
    Accept             = 'application/json'
    'OData-MaxVersion' = '4.0'
    'OData-Version'    = '4.0'
}
$api = "$OrgUrl/api/data/v9.2"

# Children before parents.
$targets = @(
    @{ Set = 'cca_itemvaluations';  Id = 'cca_itemvaluationid';  Filter = "cca_claimid eq '{0}'" },
    @{ Set = 'cca_calculationruns'; Id = 'cca_calculationrunid'; Filter = "startswith(cca_calculationname,'{0}')" },
    @{ Set = 'cca_inventoryitems';  Id = 'cca_inventoryitemid';  Filter = "cca_claimid eq '{0}'" },
    @{ Set = 'cca_approvals';       Id = 'cca_approvalid';       Filter = "startswith(cca_approvalname,'{0}')" },
    @{ Set = 'cca_caseissues';      Id = 'cca_caseissueid';      Filter = "startswith(cca_caseissuename,'{0}')" },
    @{ Set = 'cca_commandledgers';  Id = 'cca_commandledgerid';  Filter = "startswith(cca_commandname,'{0}')" },
    @{ Set = 'cca_valuationcases';  Id = 'cca_valuationcaseid';  Filter = "cca_claimid eq '{0}'" }
)

foreach ($claim in $ClaimId) {
    $safeClaim = $claim.Replace("'", "''")
    foreach ($t in $targets) {
        $filter = $t.Filter -f $safeClaim
        $url = "$api/$($t.Set)?`$select=$($t.Id)&`$filter=$([uri]::EscapeDataString($filter))"
        $rows = @()
        do {
            $response = Invoke-RestMethod -Method Get -Uri $url -Headers $headers
            $rows += $response.value
            $url = $response.'@odata.nextLink'
        } while ($url)

        foreach ($row in $rows) {
            $id = $row.($t.Id)
            if ($PSCmdlet.ShouldProcess("$($t.Set)($id)", "Delete record for $claim")) {
                Invoke-RestMethod -Method Delete -Uri "$api/$($t.Set)($id)" -Headers $headers | Out-Null
            }
        }
        Write-Host ("{0,-22} {1,4} record(s) for {2}" -f $t.Set, $rows.Count, $claim)
    }
}
