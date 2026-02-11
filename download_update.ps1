# Update Files Auto-Download Script
# This script downloads ONLY the update folder from GitHub

# Create update directory
Write-Host "Creating update directory..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "update" | Out-Null
Set-Location "update"

# Base URL for raw files
$baseUrl = "https://raw.githubusercontent.com/lee-jungkil/Lj/main/update"

# List of files to download
$files = @(
    @{Name="UPDATE.bat"; Required=$true; Size="3.0 KB"},
    @{Name="fixed_screen_display.py"; Required=$true; Size="15.9 KB"},
    @{Name="UPDATE_README.md"; Required=$false; Size="2.0 KB"},
    @{Name="SELL_HISTORY_UPDATE.md"; Required=$false; Size="4.4 KB"},
    @{Name="UPDATE_GUIDE.md"; Required=$false; Size="8.3 KB"},
    @{Name="test_sell_history.py"; Required=$false; Size="6.0 KB"}
)

Write-Host "`n============================================================" -ForegroundColor Yellow
Write-Host " Upbit AutoProfit Bot - Update Files Downloader" -ForegroundColor Yellow
Write-Host "============================================================`n" -ForegroundColor Yellow

$successCount = 0
$failCount = 0

foreach ($fileInfo in $files) {
    $file = $fileInfo.Name
    $required = $fileInfo.Required
    $size = $fileInfo.Size
    $url = "$baseUrl/$file"
    
    $status = if ($required) { "[REQUIRED]" } else { "[OPTIONAL]" }
    Write-Host "$status Downloading $file ($size)..." -ForegroundColor $(if ($required) { "Green" } else { "Gray" })
    
    try {
        Invoke-WebRequest -Uri $url -OutFile $file -ErrorAction Stop
        Write-Host "  + Downloaded successfully: $file" -ForegroundColor Green
        $successCount++
    }
    catch {
        Write-Host "  ! Failed to download: $file" -ForegroundColor Red
        Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
        $failCount++
        
        if ($required) {
            Write-Host "`n[ERROR] Required file download failed!" -ForegroundColor Red
            Write-Host "Please check your internet connection and try again." -ForegroundColor Yellow
            Write-Host "`nAlternative: Download manually from:" -ForegroundColor Yellow
            Write-Host "  $url" -ForegroundColor Cyan
        }
    }
}

Write-Host "`n============================================================" -ForegroundColor Yellow
Write-Host " Download Complete!" -ForegroundColor Yellow
Write-Host "============================================================`n" -ForegroundColor Yellow

Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Success: $successCount files" -ForegroundColor Green
Write-Host "  Failed:  $failCount files" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Gray" })
Write-Host "  Location: $PWD" -ForegroundColor Cyan

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Move this 'update' folder to your Lj-main project root" -ForegroundColor White
Write-Host "  2. Navigate to: Lj-main\update\" -ForegroundColor White
Write-Host "  3. Run: UPDATE.bat" -ForegroundColor White

Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
