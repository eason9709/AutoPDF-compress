# PDF 壓縮工具

這是一個簡單的 PDF 壓縮工具，使用 Python 和 Tkinter 開發，能夠將 PDF 檔案轉換為較小的檔案大小。

## 使用方法

1. **下載與安裝**：
   - 從 GitHub 下載此專案：
     先從螢幕右方的Release下載最新的Win11(V0.3)版本，選擇`PDFCompressor.exe`
     (Edge等瀏覽器可能會跳出不常下載等警告，您可以選擇忽略他並下載)
   - 透過下載原始碼來執行：
     考慮多數學生可能不熟悉，將暫不放出如何操作

2. **運行應用程式**：
   - 使用以下命令啟動應用程式：
     ```bash
     python autopdf.py
     ```
     前提是你有突破剛剛的困難 自己下載requirments
     
   - 或者，如果您已經打包成可執行檔，直接雙擊 `PDFCompressor.exe`。

3. **操作步驟**：
   - 在應用程式中，您可以選擇要壓縮的 PDF 檔案。
   - 設定輸出資料夾和 DPI 值。
   - 點擊「開始轉換」按鈕，應用程式將開始處理檔案。
   - 完成後，您將看到轉換後檔案的大小。

## 注意事項

- 確保您選擇的 PDF 檔案不為空，並且已選擇輸出資料夾。
- 應用程式會顯示每個檔案的轉換狀態和大小。
- 之前的版本因為沒有整合Poppler而導致無法運行，現在已經整合進到最新版本
## 貢獻

如果您有任何建議或想要貢獻，請隨時提出問題或提交拉取請求。

## 授權

本專案使用 MIT 授權，詳情請參閱 LICENSE 文件。
