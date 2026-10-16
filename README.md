# 中央極限定理 (CLT) 模擬器

依照原始 Tkinter GUI 的排列與配色製作的網頁版：上方控制列、模擬／理論統計表、四張圖及依母體變換的漸層配色。

## 🌿 [開啟線上實驗室 / Launch the simulator](https://shankao1008-ui.github.io/clt-simulator/)

網頁版在瀏覽器直接執行，不需安裝 Python、不需登入，也不會上傳抽樣資料。初次設定 GitHub Pages 後，上方連結才會生效。

### 如何探索

1. 選擇七種母體之一，調整每組樣本大小 **n** 與重複抽樣次數 **N**。
2. 比較直方圖、ECDF、常態 Q-Q 圖與盒鬚圖。
3. 點「自動播放 n」看變化，或開啟七種母體的收斂分析。
4. 固定種子可重現同一組結果；「儲存圖表」可匯出 PNG、SVG 或透過列印儲存 PDF。

**n 改變平均數的理論分配；N 改善模擬精度。** 四種主要母體為均勻、t(3)、卡方與 Beta，另提供常態、Poisson 與 Cauchy 作延伸比較。

### 首次啟用 GitHub Pages

在此 repository 的 **Settings → Pages → Build and deployment**：

- Source：**Deploy from a branch**
- Branch：**main**；Folder：**/docs**
- 按 **Save**，等待 GitHub 顯示網站網址。

之後修改 `docs/` 並提交到 main，GitHub Pages 就會重新發布。

### 本機使用網頁版

```bash
python3 -m http.server 8000 --directory docs
```

開啟 http://localhost:8000 。請透過 HTTP 伺服器或 GitHub Pages 開啟；直接雙擊 HTML 的 `file://` 模式不支援模組化 Web Worker。

### 原始 Python 桌面 GUI

網頁版是原有 Tkinter 作業的瀏覽器版本。原始 Python 程式保留在 `desktop/clt_gui.py`：

```bash
python3 -m pip install -r requirements.txt
python3 desktop/clt_gui.py
```

需要支援 Tk 的桌面 Python（例如 python.org 安裝版）；GUI 不適用於沒有桌面顯示的環境。

### 方法與限制

- 各組樣本使用獨立同分配抽樣，平均後再計算統計量。網頁版與桌面版皆預設 n=30、N=1000，固定種子預設關閉。
- SD 使用 `N-1` 分母；偏態與超額峰度為未校正的經驗中心動差比值，與原始 Python 主畫面相同定義。
- 一般母體以理論平均與理論標準誤建立常態參考。主畫面的柯西 KS、直方圖及 ECDF 參考為標準柯西；其 Q-Q 圖另以中位數與 IQR 建立穩健常態參考。
- 收斂分析每組 N=3000，八種 n、七種母體使用固定種子。柯西與穩健配適常態比較；其餘與理論常態比較。抽樣次數與 Python 版相同。
- KS 是描述距離，不使用 p 值。依原版提供探索性斜率、−1/2 參考線及抽樣誤差參考尺度；這些不是收斂速度的保證或固定下界。有限次模擬不保證曲線單調下降。
- t(3) 第三動差不存在，第四動差發散；柯西沒有有限平均數與變異數。經驗數值有限不表示母體動差存在。
- 直方圖、ECDF 與盒鬚圖以理論中心 ±4 個標準誤顯示；柯西顯示 -10 到 10。範圍外資料仍納入統計，直方圖不因截尾而重新正規化。Q-Q 顯示 1%–99% 分位數。
- 網頁版採 JavaScript 亂數與數值近似；同設定、同種子可在網頁版重現，但不與 NumPy 產生完全相同的序列。常態 CDF 採多項式近似；分位數使用 Acklam 近似。
- 模擬在 Web Worker 中運算。新設定會取消先前的計算；關閉收斂視窗可停止該分析。

### 專案結構

```text
docs/        免安裝網頁版（GitHub Pages 發布目錄）
desktop/     原始 Python GUI
tests/      網頁統計核心與瀏覽器操作測試
```

使用 Node.js 執行數值測試：`node tests/model.test.mjs`。網頁本身沒有 npm 依賴或外部 CDN。

### Credits

A statistical computing project by **shankao1008-ui**. Desktop GUI developed with assistance from Claude; browser adaptation and documentation developed with assistance from ChatGPT/Codex.

CLT theoretical reference: [Scott Sheffield, MIT 18.175 Lecture 11](https://math.mit.edu/~sheffield/2016175/Lecture11.pdf).
