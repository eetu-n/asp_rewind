import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import scipy.signal as sig
import scipy

def save_wav(signal, sr, name):
    scipy.io.wavfile.write('./audio/' + name + ".wav", sr, normalize(signal))

def sig_plot(signal, title, begi=0, endi=500, w=3.5, h=2.5, save=False, show=True, audio=False):
    # Configure matplotlib for LaTeX-style rendering
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.size": 10,
        "axes.labelsize": 10,
        "axes.titlesize": 10,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "figure.dpi": 300,
    })

    fig, ax = plt.subplots(figsize=(w, h))

    ax.plot(signal[begi:endi], color='navy')
    #ax.set_title(title)
    ax.set_xlabel(r'Sample Index')
    ax.set_ylabel(r'Amplitude')
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

    fig.tight_layout()

    if save:
        filename = './figures/' + title.replace(' ', '_').lower().replace('.', '') + '.pdf'
        fig.savefig(filename, format='pdf', bbox_inches='tight')

    if show:
        plt.show()

    if audio:
        # Assumes save_wav() is defined elsewhere
        save_wav(signal, 44100, title.replace(' ', '_').lower().replace('.', ''))

    plt.close(fig)

def bode_plot(b, fs, title, save=False, show=True, audio=False, a=1, w=3.5, h=2.5):
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.size": 10,
        "axes.labelsize": 10,
        "axes.titlesize": 10,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "figure.dpi": 300,
    })

    w_vals, h_vals = sig.freqz(b, a)
    freqs = (w_vals / (2 * np.pi)) * fs

    fig, ax = plt.subplots(figsize=(w, h))
    ax.semilogx(freqs, 20 * np.log10(abs(h_vals)), color='navy')
    #ax.set_title(title)
    ax.set_ylabel(r'Amplitude (dB)')
    ax.set_ylim(-80, 5)
    ax.set_xlabel(r'Frequency (Hz)')
    ax.set_xlim(20, 20000)
    ax.set_xticks([20, 100, 1000, 10000, 20000])
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.7)

    fig.tight_layout()

    if save:
        filename = './figures/' + title.replace(' ', '_').lower().replace('.', '') + '.pdf'
        fig.savefig(filename, format='pdf', bbox_inches='tight')

    if show:
        plt.show()

    if audio:
        save_wav(b, fs, title.replace(' ', '_').lower().replace('.', ''))

    plt.close(fig)

def fft_plot(signal, sr, title, save=False, show=True, audio=False, w=3.5, h=2.5, ylim=20000):
    import scipy.signal as sig

    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.size": 10,
        "axes.labelsize": 10,
        "axes.titlesize": 10,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "figure.dpi": 300,
    })

    f, t, Zxx = sig.stft(signal, sr, nperseg=100)

    fig, ax = plt.subplots(figsize=(w, h))
    pcm = ax.pcolormesh(t, f, np.abs(Zxx), shading='gouraud', cmap='viridis')
    #ax.set_title(title)
    ax.set_ylabel(r'Frequency (Hz)')
    ax.set_xlabel(r'Time (s)')
    ax.set_yscale('log')
    ax.set_ylim(200, 4000)
    ax.yaxis.set_major_formatter(plt.ScalarFormatter())
    ax.grid(which='both', linestyle='--', linewidth=0.5, alpha=0.5)
    pcm = ax.pcolormesh(t, f, np.abs(Zxx), shading='gouraud', cmap='viridis')
    pcm.set_rasterized(True)

    #fig.colorbar(pcm, ax=ax, format='%.0e', pad=0.02)
    fig.tight_layout()

    if save:
        filename = './figures/' + title.replace(' ', '_').lower().replace('.', '') + '.pdf'
        fig.savefig(filename, format='pdf', bbox_inches='tight')

    if show:
        plt.show()

    if audio:
        save_wav(signal, sr, title.replace(' ', '_').lower().replace('.', ''))

    plt.close(fig)

def noise(len):
    return np.random.normal(0, 1, len)

def normalize(signal):
    signal -= np.min(signal)
    signal /= np.max(signal)
    signal -= 0.5
    return signal * 2
