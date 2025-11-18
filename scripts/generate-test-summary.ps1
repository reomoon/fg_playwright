param(
    [string]$OutputPath = "output"
)

$summary = @"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FG Automation Test Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"@

$totalPassed = 0
$totalFailed = 0
$totalErrors = 0
$totalSkipped = 0
$totalTests = 0

$xmlFiles = @("precondition-results.xml", "front-results.xml", "mobile-results.xml", "va-results.xml", "wa-results.xml")

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
            $status = if ($failed -eq 0 -and $errors -eq 0) { "✅" } else { "❌" }
            
            $summary += @"
$status $($testType.ToUpper())
   Passed:  $passed
   Failed:  $failed
   Errors:  $errors
   Skipped: $skipped
   
"@
        }
    }
}

$summary += @"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Total Passed:  $totalPassed
❌ Total Failed:  $totalFailed
⚠️ Total Errors:  $totalErrors
⏭️ Total Skipped: $totalSkipped
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Grand Total:  $totalTests tests

HTML Reports:
- precondition-report.html
- front-report.html
- mobile-report.html
- va-report.html
- wa-report.html

"@

# 파일에 저장
$summary | Out-File -FilePath "$OutputPath/summary.txt" -Encoding UTF8

# GitHub Output으로 전달
Add-Content -Path $env:GITHUB_OUTPUT -Value "summary<<EOF"
Add-Content -Path $env:GITHUB_OUTPUT -Value $summary
Add-Content -Path $env:GITHUB_OUTPUT -Value "EOF"

Write-Output "Test summary generated successfully"
