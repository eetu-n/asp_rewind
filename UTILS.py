import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy

def save_wav(signal, sr, name):
    scipy.io.wavfile.write('./audio/' + name + ".wav", sr, normalize(signal))

def fft_plot(signal, sr, title, save = False, show = True, audio = False):
    import scipy.signal as sig
    f, t, Zxx = sig.stft(signal, sr, nperseg=1000)
    plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')
    plt.title(title)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.yscale('log')
    plt.ylim(20, 20000)
    if (save):
        plt.savefig('./latex/figures/' + title.replace(' ', '_').lower().replace('.', ''))
    if (show):
        plt.show()
    if (audio):
        save_wav(signal, sr, title.replace(' ', '_').lower().replace('.', ''))

def sig_plot(signal, title, save = False, show = True, audio = False):
    plt.plot(signal[:500])
    plt.title(title)
    if (save):
        plt.savefig('./latex/figures/' + title.replace(' ', '_').lower().replace('.', ''))
    if (show):
        plt.show()
    if (audio):
        save_wav(signal, 44100, title.replace(' ', '_').lower().replace('.', ''))

def bode_plot(b, fs, title, save=False, show=True, audio=False, a = 1):
    w, h = sig.freqz(b, a)
    freqs = (w / (2 * np.pi)) * fs

    fig, ax1 = plt.subplots(tight_layout=True)
    ax1.set_title(title)
    ax1.semilogx(freqs, 20 * np.log10(abs(h)), 'C0')
    ax1.set_ylabel("Amplitude (dB)", color='C0')
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_xlim(20, 20000)
    ax1.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax1.set_xticks([20, 100, 1000, 10000, 20000])
    ax1.grid(which='both', linestyle='--', linewidth=0.5)

    if (save):
        plt.savefig(title.replace(' ', '_').lower().replace('.', ''))
    if (show):
        plt.show()
    if (audio):
        save_wav(b, fs, title.replace(' ', '_').lower().replace('.', ''))

def noise(len):
    return np.random.normal(0, 1, len)

def normalize(signal):
    signal -= np.min(signal)
    signal /= np.max(signal)
    signal -= 0.5
    return signal * 2
