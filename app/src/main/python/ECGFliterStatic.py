
import numpy as np
import pywt
from scipy import signal


def butterBandPassFilter(low_cut, high_cut, sample_rate, order):
    # 生成巴特沃斯带通滤波器
    semi_sample_rate = sample_rate * 0.5
    low = low_cut / semi_sample_rate
    high = high_cut / semi_sample_rate
    b, a = signal.butter(order, [low, high], btype='bandpass')
    return b, a


def butterLowPassFilter(low_cut, sample_rate, order):
    # 生成巴特沃斯低通滤波器
    semi_sample_rate = sample_rate * 0.5
    low = low_cut / semi_sample_rate
    # high = high_cut / semi_sample_rate
    b, a = signal.butter(order, low, btype='lowpass')
    return b, a


def butterHighPassFilter(high_cut, sample_rate, order):
    # 生成巴特沃斯低通滤波器
    semi_sample_rate = sample_rate * 0.5
    # low = low_cut / semi_sample_rate
    high = high_cut / semi_sample_rate
    b, a = signal.butter(order, high, btype='highpass')
    return b, a


def butterBandStopFilter(low_cut, high_cut, sample_rate, order):
    # 生成巴特沃斯带阻滤波器
    semi_sample_rate = sample_rate * 0.5
    low = low_cut / semi_sample_rate
    high = high_cut / semi_sample_rate
    b, a = signal.butter(order, [low, high], btype='bandstop')
    return b, a


def FindMaxMin(data_filter):
    min = 65535
    max = -65535
    for item in data_filter:
        if item > max:
            max = item
        if item < min:
            min = item
    return min, max


def Filter(data, ecg_sample_rate):
    try:
        if True:
            ecg_filter = data

            b, a = butterBandStopFilter(48, 52, ecg_sample_rate, 4)
            ecg_filter = signal.filtfilt(b, a, ecg_filter)
            b, a = butterLowPassFilter(40, ecg_sample_rate, 4)
            ecg_filter = signal.filtfilt(b, a, ecg_filter)


            ks = int(ecg_sample_rate * 0.5)
            if ks % 2 == 0:
                ks -= 1
            baseline = signal.medfilt(ecg_filter, kernel_size=ks)
            ecg_filter = ecg_filter - baseline

            w = pywt.Wavelet('db6')  # 选用Daubechies8小波
            maxlev = pywt.dwt_max_level(len(ecg_filter), w.dec_len)
            print("maximum level is " + str(maxlev))
            # threshold = 0  # Threshold for filtering

            coeffs = pywt.wavedec(data=ecg_filter, wavelet='db6', level=maxlev)
            # cA4, cD4, cD3, cD2, cD1 = coeffs
            threshold = (np.median(np.abs(coeffs[len(coeffs) - 1])) / 0.6745) * (
                np.sqrt(2 * np.log(len(coeffs[len(coeffs) - 1]))))
            # # 将高频信号cD1、cD2置零
            # cD1.fill(0)
            # cD2.fill(0)
            # cD3.fill(0)
            # cD4.fill(0)
            # cD5.fill(0)
            # 将其他中低频信号按软阈值公式滤波
            for i in range(1, len(coeffs) - 1):
                coeffs[i] = pywt.threshold(coeffs[i], threshold)
            ecg_filter = pywt.waverec(coeffs=coeffs, wavelet='db6')
            ecg_filter = np.convolve(ecg_filter, np.ones((5,)) / 5, mode="vaild")


            for index in range(len(ecg_filter)):
                ecg_filter[index] = round(ecg_filter[index], 2)
            return ecg_filter.tolist()
    except:
        print("发生错误")


def run(data, ecg_sample_rate=250):
    return Filter(data, ecg_sample_rate)

# if __name__ == '__main__':
#     ecg_list = [0, 2167, 0, 0, 2167, 2165, 1410, 0, 0, 2167, 0, 0, 2167, 0, 0, 2167, 0, 0, 2167, 0, 0, 2166, 0, 0, 2167,
#                 0, 0, 2166, 0, 0, 2166, 0, 0, 2167, 0, 0, 2167, 0, 0, 2167, 0, 0, 2167, 0, 0, 2166, 0, 0, 2166, 0, 0,
#                 2167, 0, 0, 2166, 0, 0, 2166, 0, 0, 2166, 0, 0, 2166, 0, 0, 2166, 0, 0, 2166, 0, 0, 2166, 0, 0, 2167, 0,
#                 0, 2165, 0, 0, 2166, 0, 0, 2166, 0, 0, 2166, 0, 0, 2166, 2165, 607, 0, 0, 2167, 0, 0, 2166, 0, 0, 2166,
#                 0, 0, 2166, 0, 0, 2166, 2166, 453, 0, 0, 2166, 0, 0, 2166, 0, 0, 2166, 0, 0, 2167, 0, 0, 2167, 0, 0,
#                 2166, 2166, 364, 0, 0, 2166, 0, 0, 2166, 0, 0, 2167, 0, 0, 2166, 2165, 276, 0, 0, 2166, 0, 0, 2167, 0,
#                 0, 2166, 0, 0, 2166, 0, 0, 2166, 0, 0, 2166, 0, 0, 2166, 0, 0, 2167, 0, 0, 2166, 0, 0, 2166, 0, 0, 2166,
#                 0, 0, 2166, 0, 0, 2166, 0, 0, 2166, 0, 0, 2166, 0, 0, 2166, 0, 0, 2166, 0, 0, 2166, 0, 0, 2166, 0, 0,
#                 2165, 0, 0, 2166, 0, 0, 2166, 0, 0, 2166, 0, 0, 2167, 0, 0, 2165, 0, 0, 2167, 0, 0, 2166, 0, 0, 2167, 0,
#                 0, 2166, 0, 0, 2166, 0, 0, 2167, 0, 0, 2166, 0, 0, 2167, 0, 0, 2167, 0, 0, 2167, 0]
#



