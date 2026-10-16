"""中央極限定理 (CLT) 模擬器
需要套件：numpy、scipy、matplotlib（pip install numpy scipy matplotlib）
"""
import math
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import Patch
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.rcParams['font.sans-serif'] = ['PingFang TC', 'Heiti TC', 'Arial Unicode MS', 'Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# mu, sigma: 母體平均數與標準差；skew, kurt: 母體偏態與超額峰度（None 代表不存在）
DISTS = {
    "均勻分佈 U(0,1)": dict(
        mu=0.5, sigma=math.sqrt(1 / 12), skew=0.0, kurt=-1.2,
        sampler=lambda rng, N, n: rng.uniform(0, 1, (N, n)),
        cmap="viridis", line="#e63946", bg="#eef8f1",
        note="對稱、有界；本實驗中常態近似通常較快改善。"),
    "t 分佈 t(3)": dict(
        mu=0.0, sigma=math.sqrt(3), skew=None, kurt=None,
        sampler=lambda rng, N, n: rng.standard_t(3, (N, n)),
        cmap="winter", line="#d62828", bg="#eaf6ff",
        note="變異數 = 3 有限，CLT 成立；但第三動差不存在、峰度為無限大，尾巴很重，"
             "收斂較慢，且偏態與峰度的模擬值會不穩定。"),
    "卡方分佈 χ²(2)": dict(
        mu=2.0, sigma=2.0, skew=2.0, kurt=6.0,
        sampler=lambda rng, N, n: rng.chisquare(2, (N, n)),
        cmap="plasma", line="#1d3557", bg="#fff3e6",
        note="嚴重右偏（偏態 2），n 小時明顯不對稱。"),
    "貝他分佈 β(9,2)": dict(
        mu=9 / 11, sigma=math.sqrt(18 / (121 * 12)), skew=-14 * math.sqrt(12) / (13 * math.sqrt(18)), kurt=6 * (49 * 12 - 18 * 13) / (18 * 13 * 14),
        sampler=lambda rng, N, n: rng.beta(9, 2, (N, n)),
        cmap="cool", line="#ff006e", bg="#f3efff",
        note="左偏（偏態約 -0.88），有界。"),
    "常態分佈 N(5,2²)": dict(
        mu=5.0, sigma=2.0, skew=0.0, kurt=0.0,
        sampler=lambda rng, N, n: rng.normal(5.0, 2.0, (N, n)),
        cmap="turbo", line="#222222", bg="#eaf4ff",
        note="母體本身是常態，平均數在任何 n 都精確為常態。"),
    "卜瓦松分佈 Poisson(4)": dict(
        mu=4.0, sigma=2.0, skew=0.5, kurt=0.25,
        sampler=lambda rng, N, n: rng.poisson(4.0, (N, n)),
        cmap="magma", line="#2a9d8f", bg="#fff0f5",
        note="離散資料，n 小時直方圖與 KS 會受離散化影響。"),
    "柯西分佈 Cauchy（CLT 反例）": dict(
        cauchy=True, mu=0.0, sigma=None, skew=None, kurt=None,
        sampler=lambda rng, N, n: rng.standard_cauchy((N, n)),
        cmap="coolwarm", line="#111111", bg="#f4f4f4",
        note="沒有有限的平均數與變異數，CLT 不適用：n 個柯西的平均數仍是標準柯西，"
             "不論 n 多大都不會變窄或變成常態；模擬值會隨每次抽樣劇烈跳動。"),
}

N_PRESETS = [5, 10, 30, 50, 100, 300, 500, 1000]   # 作業指定的樣本數
PLAY_SEQ = [1] + N_PRESETS
BINS = 30
ANIM_STEPS = 6
ANIM_MS = 20
CAUCHY_RANGE = 10.0


def sample_means(info, rng, N, n):
    """分批抽樣，避免一次配置 N × n 的大陣列。"""
    return np.concatenate([info["sampler"](rng, min(500, N-i), n).mean(axis=1)
                           for i in range(0, N, 500)])


def fmt(v, d=3):
    return "不存在" if v is None else f"{v:.{d}f}"


def reference_normal(means, info, n):
    """回傳用來比較的常態 (loc, scale)。柯西沒有 mu/sigma，改用中位數與 IQR/1.349。"""
    if info.get("cauchy"):
        q1, med, q3 = np.percentile(means, [25, 50, 75])
        return med, (q3 - q1) / 1.349
    return info["mu"], info["sigma"] / math.sqrt(n)


def ks_normal(means, loc, scale):
    """KS 統計量：樣本對 N(loc, scale)。傳入 callable，避免新版 scipy 對 args 的相容問題。"""
    return stats.kstest(means, lambda x: stats.norm.cdf(x, loc=loc, scale=scale)).statistic


def ks_vs_reference(means, info, n):
    if info.get("cauchy"):
        return stats.kstest(means, lambda x: stats.cauchy.cdf(x)).statistic   # 對標準柯西
    loc, scale = reference_normal(means, info, n)
    return ks_normal(means, loc, scale)


class CLTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("中央極限定理 (CLT) 模擬器")
        self.root.geometry("1250x940")
        self.rng = np.random.default_rng()
        self._job = None
        self._anim_job = None
        self._play_job = None
        self.playing = False
        self.cur = None

        # ---------- 控制列 ----------
        control = tk.Frame(root, pady=6, padx=10)
        control.pack(side=tk.TOP, fill=tk.X)

        tk.Label(control, text="母體分佈:").grid(row=0, column=0, padx=5)
        self.dist_var = tk.StringVar(value="卡方分佈 χ²(2)")
        combo = ttk.Combobox(control, textvariable=self.dist_var,
                             values=list(DISTS.keys()), state="readonly", width=26)
        combo.grid(row=0, column=1, padx=5)
        combo.bind("<<ComboboxSelected>>", self.on_change)

        tk.Label(control, text="n 預設值:").grid(row=0, column=2, padx=5)
        self.preset_var = tk.StringVar(value="30")
        preset = ttk.Combobox(control, textvariable=self.preset_var,
                              values=[str(v) for v in N_PRESETS], state="readonly", width=6)
        preset.grid(row=0, column=3, padx=5)
        preset.bind("<<ComboboxSelected>>", self.on_preset)

        tk.Label(control, text="樣本大小 (n):").grid(row=0, column=4, padx=5)
        self.n_var = tk.IntVar(value=30)
        tk.Scale(control, from_=1, to=1000, orient=tk.HORIZONTAL, variable=self.n_var,
                 command=self.on_change, length=200).grid(row=0, column=5, padx=5)

        tk.Label(control, text="抽樣次數 (N):").grid(row=0, column=6, padx=5)
        self.N_var = tk.IntVar(value=1000)
        tk.Scale(control, from_=100, to=10000, resolution=100, orient=tk.HORIZONTAL,
                 variable=self.N_var, command=self.on_change, length=200).grid(row=0, column=7, padx=5)

        btns = tk.Frame(root, padx=10)
        btns.pack(side=tk.TOP, fill=tk.X)
        self.play_btn = tk.Button(btns, text="▶ 自動播放 n", command=self.toggle_play, padx=6)
        self.play_btn.pack(side=tk.LEFT, padx=4)
        tk.Button(btns, text="收斂速度分析", command=self.show_convergence, padx=6).pack(side=tk.LEFT, padx=4)
        tk.Button(btns, text="儲存圖表", command=self.save_figure, padx=6).pack(side=tk.LEFT, padx=4)
        self.seed_var = tk.BooleanVar(value=False)
        tk.Checkbutton(btns, text="固定隨機種子（結果可重現）", variable=self.seed_var,
                       command=self.on_change).pack(side=tk.LEFT, padx=12)

        # ---------- 統計指標表 ----------
        table = tk.Frame(root, padx=10, pady=4)
        table.pack(side=tk.TOP, fill=tk.X)
        heads = ["", "平均數", "標準誤", "偏態", "超額峰度", "KS 距離"]
        for c, h in enumerate(heads):
            tk.Label(table, text=h, font=("", 11, "bold"), width=16).grid(row=0, column=c)
        self.sim_vars = [tk.StringVar() for _ in range(5)]
        self.th_vars = [tk.StringVar() for _ in range(5)]
        tk.Label(table, text="模擬值", fg="#1d6fb8", font=("", 11, "bold")).grid(row=1, column=0)
        tk.Label(table, text="理論值", fg="#c0392b", font=("", 11, "bold")).grid(row=2, column=0)
        for c in range(5):
            tk.Label(table, textvariable=self.sim_vars[c], fg="#1d6fb8", width=16).grid(row=1, column=c + 1)
            tk.Label(table, textvariable=self.th_vars[c], fg="#c0392b", width=16).grid(row=2, column=c + 1)
        self.note_var = tk.StringVar()
        tk.Label(table, textvariable=self.note_var, fg="#555555", anchor="w", justify="left",
                 wraplength=1180).grid(row=3, column=0, columnspan=6, sticky="w", pady=(4, 0))

        # ---------- 2x2 圖表 ----------
        self.fig = Figure(figsize=(10, 7.4))
        self.fig.subplots_adjust(left=0.07, right=0.97, top=0.89, bottom=0.07, hspace=0.38, wspace=0.2)
        self.ax = self.fig.add_subplot(2, 2, 1)         # 直方圖（有動畫）
        self.ax_ecdf = self.fig.add_subplot(2, 2, 2)    # 經驗 CDF
        self.ax_qq = self.fig.add_subplot(2, 2, 3)      # Q-Q 圖
        self.ax_box = self.fig.add_subplot(2, 2, 4)     # 盒鬚圖
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.bars = self.ax.bar(np.arange(BINS), np.zeros(BINS), width=1.0,
                                align="edge", edgecolor="white", linewidth=0.6)
        (self.line,) = self.ax.plot([], [], lw=2.8)
        self.fill = self.ax.fill_between([0, 1], [0, 0], alpha=0.0)
        self.proxy = Patch(label="樣本平均數的直方圖")
        self.line.set_label("理論曲線")
        self.legend = self.ax.legend(handles=[self.proxy, self.line], loc="upper right", fontsize=8)
        self.ax.set_xlabel("樣本平均數")
        self.ax.set_ylabel("頻率密度")
        self.ax.grid(alpha=0.25)

        self.plot_clt()

    # ---------- 事件 ----------
    def on_change(self, *args):
        if self._job is None:
            self._job = self.root.after_idle(self.plot_clt)

    def on_preset(self, *args):
        self.n_var.set(int(self.preset_var.get()))
        self.on_change()

    def toggle_play(self):
        if self.playing:
            self.stop_play()
        else:
            self.playing = True
            self.play_btn.config(text="■ 停止")
            self.play_idx = 0
            self.play_step()

    def stop_play(self):
        self.playing = False
        self.play_btn.config(text="▶ 自動播放 n")
        if self._play_job is not None:
            self.root.after_cancel(self._play_job)
            self._play_job = None

    def play_step(self):
        if not self.playing:
            return
        if self.play_idx >= len(PLAY_SEQ):
            self.stop_play()
            return
        self.n_var.set(PLAY_SEQ[self.play_idx])
        self.play_idx += 1
        self.plot_clt()
        self._play_job = self.root.after(900, self.play_step)

    # ---------- 模擬與繪圖 ----------
    def plot_clt(self):
        self._job = None
        dist_type = self.dist_var.get()
        n, N = self.n_var.get(), self.N_var.get()
        info = DISTS[dist_type]
        cauchy = info.get("cauchy", False)
        rng = np.random.default_rng(42) if self.seed_var.get() else self.rng

        means = sample_means(info, rng, N, n)
        loc, scale = reference_normal(means, info, n)

        if cauchy:
            edges = np.linspace(-CAUCHY_RANGE, CAUCHY_RANGE, BINS + 1)
            mu_t, se_t = 0.0, 1.0
        else:
            mu_t, se_t = info["mu"], info["sigma"] / math.sqrt(n)   # 理論 mu, sigma/sqrt(n)
            edges = np.linspace(mu_t - 4 * se_t, mu_t + 4 * se_t, BINS + 1)
        counts, _ = np.histogram(means, bins=edges)
        heights = counts / (N * np.diff(edges))
        target = (edges, heights.astype(float), mu_t, se_t)

        self.theme = info
        self.cmap = matplotlib.colormaps[info["cmap"]]
        self.fig.set_facecolor(info["bg"])
        for a in (self.ax, self.ax_ecdf, self.ax_qq, self.ax_box):
            a.set_facecolor("white")
        self.line.set_color(info["line"])
        self.proxy.set_facecolor(self.cmap(0.6))
        self.fig.suptitle(f"中央極限定理 - {dist_type}　（n={n}, N={N}）",
                          color=info["line"], fontweight="bold", fontsize=13)
        self.ax.set_title("直方圖 vs 理論曲線", fontsize=10)
        label = ("理論：標準柯西（不隨 n 變窄）" if cauchy else
                 rf"理論常態 $\mu={mu_t:.3f}$, $\sigma/\sqrt{{n}}={se_t:.3f}$")
        self.legend.get_texts()[1].set_text(label)

        self.update_table(means, info, n, N, cauchy, mu_t, se_t)
        self.draw_side_panels(means, info, cauchy, loc, scale, edges)

        if self.cur is None:
            self.cur = target
            self.render(target)
        else:
            self.animate_to(target)

    def update_table(self, means, info, n, N, cauchy, mu_t, se_t):
        m, s = means.mean(), means.std(ddof=1)
        sk, ku = stats.skew(means), stats.kurtosis(means)    # kurtosis 預設即超額峰度
        ks = ks_vs_reference(means, info, n)
        floor = 0.87 / math.sqrt(N)                           # 連續虛無分配下 KS 抽樣誤差的參考尺度，非下界
        sim = [fmt(m), fmt(s), fmt(sk), fmt(ku), fmt(ks)]
        if cauchy:
            th = ["不存在", "不存在", "不存在", "不存在", f"對標準柯西 ≈{floor:.3f}"]
        else:
            th_sk = None if info["skew"] is None else info["skew"] / math.sqrt(n)
            th_ku = None if info["kurt"] is None else info["kurt"] / n
            th = [fmt(mu_t), fmt(se_t), fmt(th_sk), fmt(th_ku), f"→ 0（雜訊約 {floor:.3f}）"]
        for v, t in zip(self.sim_vars, sim):
            v.set(t)
        for v, t in zip(self.th_vars, th):
            v.set(t)
        self.note_var.set(info["note"] + "　｜　理論偏態 = γ/√n、理論超額峰度 = κ/n；"
                          "KS 對照：一般母體為理論常態，柯西為標準柯西；收斂分析中的柯西另與穩健配適常態比較。")

    def draw_side_panels(self, means, info, cauchy, loc, scale, edges):
        color = info["line"]
        cm = self.cmap(0.6)
        N = len(means)

        # 經驗 CDF vs 理論 CDF
        ax = self.ax_ecdf
        ax.clear()
        xs = np.sort(means)
        idx = np.arange(N)
        ax.step(xs[idx], (idx + 1) / N, where="post", color=cm, lw=2, label="Empirical CDF")
        xg = np.linspace(edges[0], edges[-1], 300)
        ref = stats.cauchy.cdf(xg) if cauchy else stats.norm.cdf(xg, loc=loc, scale=scale)
        ax.plot(xg, ref, "--", color=color, lw=2.5, alpha=0.8, label="理論 CDF")
        ax.set_xlim(edges[0], edges[-1])
        ax.set_title("經驗累積分配函數 (ECDF)", fontsize=10)
        ax.legend(fontsize=8, loc="lower right")
        ax.grid(alpha=0.25)

        # Q-Q 圖（對常態；柯西用穩健配適的常態）
        ax = self.ax_qq
        ax.clear()
        p = np.linspace(0.01, 0.99, 200)
        theo = stats.norm.ppf(p, loc=loc, scale=scale)
        samp = np.quantile(means, p)
        ax.scatter(theo, samp, s=12, color=cm)
        lo, hi = min(theo.min(), samp.min()), max(theo.max(), samp.max())
        ax.plot([lo, hi], [lo, hi], "--", color=color, lw=2)
        ax.set_title("Q-Q 圖（對常態" + ("，柯西為穩健配適" if cauchy else "") + "）", fontsize=10)
        ax.set_xlabel("理論分位數", fontsize=9)
        ax.set_ylabel("樣本分位數", fontsize=9)
        ax.grid(alpha=0.25)

        # 盒鬚圖
        ax = self.ax_box
        ax.clear()
        ax.boxplot(means, **({"orientation": "horizontal"} if "orientation" in __import__("inspect").signature(ax.boxplot).parameters else {"vert": False}), notch=True, patch_artist=True,
                   boxprops=dict(facecolor=cm, alpha=0.8),
                   medianprops=dict(color=color, lw=2),
                   flierprops=dict(marker="o", markersize=2, markerfacecolor=cm,
                                   markeredgecolor=cm, alpha=0.4))
        ax.set_xlim(edges[0], edges[-1])
        ax.set_yticks([])
        ax.set_title("盒鬚圖", fontsize=10)
        ax.grid(alpha=0.25)

    # ---------- 動畫（直方圖形變）----------
    def animate_to(self, target):
        if self._anim_job is not None:
            self.root.after_cancel(self._anim_job)
        start = self.cur

        def step(i):
            t = i / ANIM_STEPS
            e = 1 - (1 - t) ** 3
            state = tuple(a + (b - a) * e for a, b in zip(start, target))
            self.cur = state
            self.render(state)
            if i < ANIM_STEPS:
                self._anim_job = self.root.after(ANIM_MS, step, i + 1)
            else:
                self._anim_job = None

        step(1)

    def render(self, state):
        edges, heights, mu, se = state
        cauchy = self.theme.get("cauchy", False)
        x = np.linspace(edges[0], edges[-1], 300)
        if cauchy:
            pdf = 1.0 / (np.pi * (1 + x ** 2))
        else:
            pdf = np.exp(-0.5 * ((x - mu) / se) ** 2) / (se * np.sqrt(2 * np.pi))
        ymax = max(heights.max(), pdf.max()) * 1.2

        for k, rect in enumerate(self.bars):
            rect.set_x(edges[k])
            rect.set_width(edges[k + 1] - edges[k])
            rect.set_height(heights[k])
            rect.set_facecolor(self.cmap(0.15 + 0.8 * min(heights[k] / ymax * 1.2, 1.0)))

        self.line.set_data(x, pdf)
        self.fill.remove()
        self.fill = self.ax.fill_between(x, pdf, color=self.theme["line"], alpha=0.12)
        self.ax.set_xlim(edges[0], edges[-1])
        self.ax.set_ylim(0, ymax)
        self.canvas.draw()

    # ---------- 收斂速度分析：所有分佈放在同一張 log-log 圖 ----------
    def show_convergence(self):
        self.root.config(cursor="watch")
        self.root.update()
        try:
            Nc = 3000
            floor = 0.87 / math.sqrt(Nc)
            palette = plt.get_cmap("tab10")
            rng = np.random.default_rng(7)
            results = {}
            for name, info in DISTS.items():
                ks_list = []
                for n in N_PRESETS:
                    means = sample_means(info, rng, Nc, n)
                    if info.get("cauchy"):
                        # 與穩健配適的常態比較，看它是否越來越像常態（答案：不會）
                        loc, scale = reference_normal(means, info, n)
                        ks = ks_normal(means, loc, scale)
                    else:
                        ks = ks_vs_reference(means, info, n)
                    ks_list.append(ks)
                results[name] = np.array(ks_list)
        finally:
            self.root.config(cursor="")

        win = tk.Toplevel(self.root)
        win.title("收斂速度分析")
        win.geometry("860x640")
        fig = Figure(figsize=(8.4, 6), layout="constrained")
        ax = fig.add_subplot(111)
        ns = np.array(N_PRESETS, float)
        for i, (name, ks) in enumerate(results.items()):
            mask = ks > 1.5 * floor
            if mask.sum() >= 3:
                slope = np.polyfit(np.log(ns[mask]), np.log(ks[mask]), 1)[0]
                lab = f"{name}（斜率 {slope:.2f}）"
            else:
                lab = f"{name}（斜率：接近抽樣誤差尺度）"
            style = "x--" if DISTS[name].get("cauchy") else "o-"
            ax.loglog(ns, ks, style, lw=2, color=palette(i), label=lab)
        ref0 = max(results[k][0] for k in results if not DISTS[k].get("cauchy"))
        ax.loglog(ns, ref0 * (ns / ns[0]) ** -0.5, ":", color="gray", lw=2, label="參考斜率 −1/2")
        ax.axhline(floor, ls=":", color="#c0392b", label=f"抽樣誤差參考尺度 ≈ {floor:.3f}")
        ax.set_title("各母體分佈的 KS 距離隨 n 的變化（越低越像常態）", fontweight="bold")
        ax.set_xlabel("樣本大小 n（log）")
        ax.set_ylabel("KS 距離（log）")
        ax.set_xticks(N_PRESETS)
        ax.set_xticklabels([str(v) for v in N_PRESETS])
        ax.grid(alpha=0.3, which="both")
        ax.legend(fontsize=8)
        cv = FigureCanvasTkAgg(fig, master=win)
        cv.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        cv.draw()

    def save_figure(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG 圖片", "*.png"), ("PDF", "*.pdf"), ("SVG", "*.svg")],
            initialfile="clt_plot.png", title="儲存圖表")
        if not path:
            return
        try:
            self.fig.savefig(path, dpi=200, facecolor=self.fig.get_facecolor())
            messagebox.showinfo("儲存成功", f"已儲存至：\n{path}")
        except Exception as e:
            messagebox.showerror("儲存失敗", str(e))


# 原始 GUI 由使用者提供的 Claude 程式改寫；統計標示與記憶體使用已修正。
# 執行：python CLT_GUI_學號.py
# 安裝：python -m pip install numpy scipy matplotlib
# 需要含 Tk 支援的 Python；macOS 可使用 python.org 安裝版。
if __name__ == "__main__":
    root = tk.Tk()
    CLTApp(root)
    root.mainloop()