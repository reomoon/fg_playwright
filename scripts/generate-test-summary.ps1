param(
    [string]$OutputPath = "output"
)

# 현재 시간 가져오기
$startTime = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")

$summary = "FG Automation Test Results ($startTime)`n" +
           "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n`n"

$totalPassed = 0
$totalFailed = 0
$totalErrors = 0
$totalSkipped = 0
$totalTests = 0

$xmlFiles = @("precondition-results.xml", "front-results.xml", "mobile-results.xml", "va-results.xml", "wa-results.xml")
$testLabels = @{
    "precondition" = "[PRECONDITION]"
    "front"       = "[FRONT]"
    "mobile"      = "[MOBILE]"
    "va"          = "[VENDOR ADMIN]"
    "wa"          = "[WEB ADMIN]"
}

foreach ($xmlFile in $xmlFiles) {
    $path = "$OutputPath/$xmlFile"
    if (Test-Path $path) {
        [xml]$xml = Get-Content $path
        $testsuite = $xml.testsuites.testsuite
        
        foreach ($xmlFile in $xmlFiles) {

    $summary += "Pytest Case Summary`n"

    $caseGroups = @{}
    foreach ($case in $testcases) {
        $file = $case.file
        if (-not $file) { continue }
        $filename = [System.IO.Path]::GetFileName($file)
        if (-not $caseGroups.ContainsKey($filename)) {
            $caseGroups[$filename] = @{fail=0}
        }
        if ($case.failure -or $case.error) {
            $caseGroups[$filename].fail++
        }
    }

    foreach ($filename in $caseGroups.Keys) {
        $g = $caseGroups[$filename]
        $result = if ($g.fail -eq 0) { "Pass" } else { "❌ Fail" }
        $summary += "$filename : $result`n"
    }
    $summary += "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n"
}

# 전체 요약 계산

$overallStatus = if ($totalFailed -eq 0 -and $totalErrors -eq 0) { "✅ PASSED" }
                 elseif ($totalFailed -le 5) { "⚠️ NEEDS REVIEW" }
                 else { "❌ FAILED" }
$passRate = if ($totalTests -gt 0) { [math]::Round(($totalPassed / $totalTests) * 100, 1) } else { 0 }

$summary += @"
Total Summary
Status: $overallStatus
Pass Rate: $passRate%

✓ Passed: $totalPassed
✗ Failed: $totalFailed
⚠ Errors: $totalErrors
⊘ Skipped: $totalSkipped
Total Tests: $totalTests

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"@

# 파일에 저장
$summary | Out-File -FilePath "$OutputPath/summary.txt" -Encoding UTF8

# GitHub Output으로 전달
Add-Content -Path $env:GITHUB_OUTPUT -Value "summary<<EOF"
Add-Content -Path $env:GITHUB_OUTPUT -Value $summary
Add-Content -Path $env:GITHUB_OUTPUT -Value "EOF"

Write-Output "Test summary generated successfully!"