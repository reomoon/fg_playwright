param(
    [string]$OutputPath = "output"
)

# 현재 시간 가져오기
$startTime = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")

$summary = @"
[FG Automation] Test Results
Started at: $startTime

"@

$totalPassed = 0
$totalFailed = 0
$totalErrors = 0
$totalSkipped = 0
$totalTests = 0

$xmlFiles = @("precondition-results.xml", "front-results.xml", "mobile-results.xml", "va-results.xml", "wa-results.xml")
$testLabels = @{
    "precondition" = "PRECONDITION"
    "front"       = "Front"
    "mobile"      = "MOBILE"
    "va"          = "VENDOR ADMIN"
    "wa"          = "WEB ADMIN"
}

foreach ($xmlFile in $xmlFiles) {
    $path = "$OutputPath/$xmlFile"
    if (Test-Path $path) {
        [xml]$xml = Get-Content $path
        $testsuite = $xml.testsuites.testsuite
        
        if ($testsuite -ne $null) {
            $total = [int]$testsuite.tests
            $passed = $total - [int]$testsuite.failures - [int]$testsuite.errors - [int]$testsuite.skipped
            $failed = [int]$testsuite.failures
            $errors = [int]$testsuite.errors
            $skipped = [int]$testsuite.skipped
            
            $totalPassed += $passed
            $totalFailed += $failed
            $totalErrors += $errors
            $totalSkipped += $skipped
            $totalTests += $total
            
            $testType = $xmlFile -replace "-results.xml"
            $label = $testLabels[$testType]
            $statusIcon = if ($failed -eq 0 -and $errors -eq 0) { "✅" } else { "❌" }
            
            $summary += @"
$statusIcon $label
   ✓ Passed: $passed  |  ✗ Failed: $failed  |  ⚠ Errors: $errors  |  ⊘ Skipped: $skipped

"@
        }
    }
}

$overallStatus = if ($totalFailed -eq 0 -and $totalErrors -eq 0) { "✅ PASSED" } else { "❌ FAILED" }
$passRate = if ($totalTests -gt 0) { [math]::Round(($totalPassed / $totalTests) * 100, 1) } else { 0 }

$summary += @"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOTAL SUMMARY
Status: $overallStatus
Pass Rate: $passRate%

✓ Passed: $totalPassed  |  ✗ Failed: $totalFailed  |  ⚠ Errors: $totalErrors  |  ⊘ Skipped: $totalSkipped
Total Tests: $totalTests

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"@

# 파일에 저장
$summary | Out-File -FilePath "$OutputPath/summary.txt" -Encoding UTF8

# GitHub Output으로 전달
Add-Content -Path $env:GITHUB_OUTPUT -Value "summary<<EOF"
Add-Content -Path $env:GITHUB_OUTPUT -Value $summary
Add-Content -Path $env:GITHUB_OUTPUT -Value "EOF"

Write-Output "Test summary generated successfully!"