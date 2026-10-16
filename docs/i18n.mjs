// Translate presentation text only; never change simulation data or control values.
const translations = [["曲線可能因抽樣誤差起伏。柯西與中位數及 IQR 配適的常態比較，其餘使用理論常態。斜率與抽樣誤差尺度僅供探索，不是收斂速度的保證或 KS 下界。", "Curves may fluctuate because of sampling error. Cauchy is compared with a normal distribution fitted using the median and IQR; other populations use the theoretical normal reference. Slopes and sampling-error scales are exploratory, not guaranteed convergence rates or lower bounds on KS distance."], ["理論偏態 = γ/√n、理論超額峰度 = κ/n（相關動差存在時）；KS 對照：一般母體為理論常態，柯西為標準柯西。", "Theoretical skewness = γ/√n and excess kurtosis = κ/n when the relevant moments exist. KS reference: theoretical normal for other populations; standard Cauchy for Cauchy."], ["各母體分佈的 KS 距離隨 n 的變化（越低越像常態） · 每組 N=3000", "KS distance versus n for each population (lower means closer to normal) · N=3000 per setting"], ["變異數有限，因此 CLT 成立；但重尾會讓模擬標準差與尾部較不穩定。", "Finite variance allows the CLT to apply, but heavy tails make simulated standard deviations and tail behavior less stable."], ["CLT 條件不成立：沒有有限平均數與變異數，平均數仍為標準柯西。", "The CLT assumptions fail: neither a finite mean nor variance exists. Sample means remain standard Cauchy."], ["從右偏到接近對稱。增加 n，觀察平均數與常態曲線逐漸靠攏。", "From right-skewed to nearly symmetric: increase n to see sample means approach the normal reference."], ["全部資料均納入統計。Q-Q 圖顯示 1%–99% 分位數。", "All observations are included in statistics. Q-Q plots show the 1st–99th percentiles."], ["母體本身為常態：任何 n 下，平均數都精確服從常態分配。", "The population is normal, so sample means are exactly normally distributed for every n."], ["完成 · 每組 N=3000 · 固定種子 · 七種母體", "Complete · N=3000 per setting · Fixed seed · Seven populations"], ["左偏且有界。和卡方分配一起比較不同偏斜方向的影響。", "Left-skewed and bounded. Compare with chi-square to explore opposite directions of skewness."], ["離散母體。小 n 時的階梯與間隙是分配本身的特性。", "A discrete population. Steps and gaps at small n are features of the distribution."], ["柯西的 Q-Q 圖使用中位數與 IQR 配適常態。", "The Cauchy Q-Q plot uses a normal reference fitted with the median and IQR."], ["灰線：參考斜率 −1/2　紅線：抽樣誤差參考尺度", "Gray: reference slope −1/2 · Red: sampling-error reference scale"], ["請使用支援 Web Worker 的現代瀏覽器。", "Please use a modern browser with Web Worker support."], ["盒鬚圖，鬚線至 1.5 IQR 範圍內最遠觀測", "Box plot: whiskers reach the most extreme observations within 1.5 IQR"], ["對稱、有界。觀察平均數如何逐漸形成鐘形分配。", "Symmetric and bounded. Watch the distribution of sample means become bell-shaped."], ["常態 Q-Q 圖（1%–99% 分位數）", "Normal Q-Q plot (1st–99th percentiles)"], ["Q-Q 圖（對常態，柯西為穩健配適）", "Normal Q-Q plot (robust fit for Cauchy)"], ["PNG 匯出失敗，請使用 SVG。", "PNG export failed. Please use SVG."], ["中央極限定理 (CLT) 模擬器", "Central Limit Theorem (CLT) Simulator"], ["無法啟動模擬，請重新整理頁面。", "Unable to start the simulation. Please reload the page."], ["經驗累積分配函數 (ECDF)", "Empirical cumulative distribution (ECDF)"], ["固定隨機種子（結果可重現）", "Fixed random seed (reproducible results)"], ["七種分配的 KS 收斂比較", "KS convergence comparison across seven distributions"], ["運算失敗，請關閉後重試。", "Calculation failed. Close this dialog and try again."], ["直方圖 vs 理論曲線", "Histogram vs. theoretical density"], ["Q-Q 圖（對常態）", "Normal Q-Q plot"], ["GitHub 原始碼", "Source on GitHub"], ["樣本平均數的直方圖", "Histogram of sample means"], ["模擬與理論統計指標", "Simulated and theoretical statistics"], ["樣本大小 (n):", "Sample size (n):"], ["抽樣次數 (N):", "Repetitions (N):"], ["接近抽樣誤差尺度", "near sampling-error scale"], ["樣本平均數直方圖", "Histogram of sample means"], ["經驗累積分配函數", "Empirical cumulative distribution"], ["（CLT 反例）", " (CLT counterexample)"], ["理論：標準柯西", "Theoretical: standard Cauchy"], ["常態理論分位數", "Normal theoretical quantiles"], ["選擇輸出格式：", "Choose an export format:"], ["PDF（列印）", "PDF (print)"], ["中央極限定理", "Central Limit Theorem"], ["關閉收斂分析", "Close convergence analysis"], ["收斂速度分析", "Convergence analysis"], ["n 預設值:", "Preset n:"], ["自動播放 n", "Animate n"], ["理論常態參考", "Theoretical normal reference"], ["標準柯西參考", "Standard Cauchy reference"], ["理論 CDF", "Theoretical CDF"], ["PNG 圖片", "PNG image"], ["SVG 圖片", "SVG image"], ["卜瓦松分佈", "Poisson"], ["卜瓦松分配", "Poisson"], ["母體分佈:", "Population:"], ["準備模擬…", "Preparing simulation…"], ["正在抽樣…", "Sampling…"], ["等待更新…", "Waiting for update…"], ["KS 距離", "KS distance"], ["對標準柯西", "vs. standard Cauchy"], ["抽樣誤差約", "sampling error ≈"], ["樣本平均數", "Sample mean"], ["樣本分位數", "Sample quantiles"], ["顯示範圍外", "Outside displayed range: "], ["準備運算…", "Preparing calculation…"], ["均勻分佈", "Uniform"], ["t 分佈", "Student’s t"], ["卡方分佈", "Chi-square"], ["貝他分佈", "Beta"], ["常態分佈", "Normal"], ["柯西分佈", "Cauchy"], ["均勻分配", "Uniform"], ["t 分配", "Student’s t"], ["卡方分配", "Chi-square"], ["貝他分配", "Beta"], ["常態分配", "Normal"], ["柯西分配", "Cauchy"], ["停止播放", "Stop animation"], ["儲存圖表", "Save charts"], ["模擬設定", "Simulation settings"], ["模擬圖表", "Simulation charts"], ["模擬完成", "Simulation complete"], ["超額峰度", "Excess kurtosis"], ["頻率密度", "Density"], ["累積機率", "Cumulative probability"], ["理論常態", "Theoretical normal"], ["計算中…", "Calculating…"], ["平均數", "Mean"], ["標準誤", "Standard error"], ["模擬值", "Simulated"], ["理論值", "Theoretical"], ["不存在", "Undefined"], ["盒鬚圖", "Box plot"], ["斜率 ", "slope "], ["偏態", "Skewness"], ["取消", "Cancel"]];
let language = 'zh';
try { language = localStorage.getItem('clt-language') === 'en' ? 'en' : 'zh'; } catch {}
export function translate(text) {
  if (language !== 'en') return text;
  // One pass prevents translated fragments from being translated again.
  return text.replace(pattern, match => dictionary.get(match));
}
const dictionary = new Map(translations);
const pattern = new RegExp(translations.map(([s])=>s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|'), 'g');
const originals = new WeakMap();
function apply() {
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    if (['SCRIPT','STYLE'].includes(node.parentElement?.tagName) || node.parentElement?.closest('#language-picker')) continue;
    let entry = originals.get(node);
    if (!entry || node.nodeValue !== entry.output) entry = {source:node.nodeValue};
    entry.output = translate(entry.source);
    if (node.nodeValue !== entry.output) node.nodeValue = entry.output;
    originals.set(node,entry);
  }
  for (const el of document.querySelectorAll('[aria-label]')) {
    let entry = originals.get(el);
    if (!entry || el.getAttribute('aria-label') !== entry.output) entry = {source:el.getAttribute('aria-label')};
    entry.output = translate(entry.source);
    if (el.getAttribute('aria-label') !== entry.output) el.setAttribute('aria-label',entry.output);
    originals.set(el,entry);
  }
  document.documentElement.lang = language === 'en' ? 'en' : 'zh-Hant';
  document.title = translate('中央極限定理 (CLT) 模擬器');
}
export function initLanguage() {
  const select = document.getElementById('language');
  select.value = language;
  select.addEventListener('change', () => {
    language = select.value;
    try { localStorage.setItem('clt-language',language); } catch {}
    apply();
  });
  apply();
  new MutationObserver(apply).observe(document.body,{subtree:true,childList:true,characterData:true});
}
