import numpy as np
import scipy.stats as stats
import math
from collections import Counter

class WeakPRNGLGC:
    def __init__(self, a, b, p, seed=1234):
        self.a = a
        self.b = b
        self.p = p
        self.seed = seed
        self.generated_numbers = []

    def generate_numbers(self, n):
        """Genera una secuencia de números pseudoaleatorios"""
        r = [self.seed]
        for i in range(1, n):
            gen = (self.a * r[i-1] * self.b) % self.p
            r.append(gen)
        self.generated_numbers = r
        return r

    def chi_square_test(self, num_bins=10):
        """Realiza el test de Chi-cuadrado sobre los números generados"""
        data = self.generated_numbers
        min_value = min(data)
        max_value = max(data)
        bin_width = (max_value - min_value + 1) // num_bins
        bins = [min_value + i * bin_width for i in range(num_bins + 1)]
        frequencies = [0] * num_bins
        for num in data:
            index = (num - min_value) // bin_width
            if index == num_bins:
                index -= 1
            frequencies[index] += 1
        expected_frequency = len(data) / num_bins
        chi_squared_stat = sum([(f - expected_frequency)**2 / expected_frequency for f in frequencies])
        p_value = 1 - stats.chi2.cdf(chi_squared_stat, num_bins - 1)
        return chi_squared_stat, p_value

    def autocorrelation(self, lag=1):
        """Calcula la autocorrelación de los números generados"""
        data = self.generated_numbers
        mean = np.mean(data)
        autocorr = np.corrcoef(data[:-lag], data[lag:])[0][1]
        return autocorr

    def entropy(self):
        """Calcula la entropía de los números generados"""
        data = self.generated_numbers
        n = len(data)
        count = Counter(data)
        prob = [freq / n for freq in count.values()]
        entropy_value = -sum(p * math.log2(p) for p in prob)
        return entropy_value


# Parámetros
a = 30
b = 72
p = 104743
num_numbers = 1000000

prng = WeakPRNGLGC(a, b, p)
pseudo_random_numbers = prng.generate_numbers(num_numbers)
print("Números pseudoaleatorios generados:", pseudo_random_numbers[:10])
chi_stat, chi_p_value = prng.chi_square_test()
print(f"Estadística Chi-cuadrado: {chi_stat}, p-valor: {chi_p_value}")
autocorr_value = prng.autocorrelation()
print(f"Autocorrelación (lag=1): {autocorr_value}")
entropy_value = prng.entropy()
print(f"Entropía de la secuencia: {entropy_value}")
