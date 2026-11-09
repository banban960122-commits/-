"""第01讲 数制转换与存储容量估算。

运行方法：python estimate.py
仅使用Python 3标准库，无须安装依赖。
步骤1—6使用实验指南参数；照片对比及拓展采用示例数据。
"""

from fractions import Fraction


def size_line(name, byte_count):
    print(f'{name}: {byte_count:,} B = {byte_count / 10**6:.6f} MB'
          f' = {byte_count / 2**20:.6f} MiB')


def main():
    print('=== Steps 1-3: number conversion ===')
    binary = int('10110101', 2)
    hexadecimal = hex(255)
    converted = bin(int('1A', 16))
    padded = format(int('1A', 16), '08b')
    print("int('10110101', 2) =", binary)
    print('hex(255) =', hexadecimal)
    print("bin(int('1A', 16)) =", converted)
    print("format(int('1A', 16), '08b') =", padded)

    print('\n=== Steps 4-6: storage estimates ===')
    print('1 B = 8 bit; 1 MB = 10^6 B; 1 MiB = 2^20 B')
    print('1 GB = 10^9 B; 1 GiB = 2^30 B')
    photo = 1920 * 1080 * 24 // 8
    audio = 240 * 44100 * 16 * 2 // 8
    movie = 7200 * 8_000_000 // 8
    size_line('RGB24 photo', photo)
    size_line('PCM audio', audio)
    print(f'Movie: {movie:,} B = {movie / 10**9:.6f} GB'
          f' = {movie / 2**30:.6f} GiB')
    print('Photo/PCM exclude headers; 8 Mbps is the average TOTAL movie bitrate.')

    print('\n=== Step 7: illustrative photo data (not phone measurements) ===')
    width, height, bit_depth, jpeg_bytes = 4000, 3000, 24, 4_500_000
    raw = width * height * bit_depth // 8
    ratio = Fraction(raw, jpeg_bytes)
    reduction = (1 - Fraction(jpeg_bytes, raw)) * 100
    size_line('RGB24 reference', raw)
    size_line('Example JPEG', jpeg_bytes)
    print(f'Reference/file ratio = {float(ratio):.6f}')
    print(f'Storage reduction = {float(reduction):.4f}%')

    print('\n=== Extension: illustrative 256 GB storage budget ===')
    samples = [3_800_000, 4_200_000, 4_500_000, 4_800_000, 5_200_000]
    mean = Fraction(sum(samples), len(samples))
    budget = (256 - 40 - 16) * 10**9
    count = budget // mean
    print('Sample sizes (B):', samples)
    print(f'Samples = {len(samples)}; total = {sum(samples):,} B')
    print(f'Mean = {float(mean):,.0f} B/photo')
    print('Assumptions: other occupied = 40 GB; reserve = 16 GB')
    print(f'Photo budget = {budget:,} B = {budget / 10**9:.0f} GB')
    print(f'Estimated photo count = {count:,}')
    print(f'At 3 MB/photo: {budget // 3_000_000:,} photos')
    print(f'At 6 MB/photo: {budget // 6_000_000:,} photos')

    checks = [
        ('binary to decimal', binary == 181),
        ('decimal to hexadecimal', hexadecimal == '0xff'),
        ('hexadecimal to binary', converted == '0b11010'),
        ('8-bit format', padded == '00011010'),
        ('RGB24 photo bytes', photo == 6_220_800),
        ('PCM audio bytes', audio == 42_336_000),
        ('movie bytes', movie == 7_200_000_000),
        ('example raw bytes', raw == 36_000_000),
        ('example capacity ratio', ratio == 8),
        ('example reduction', reduction == Fraction(175, 2)),
        ('mean sample size', mean == 4_500_000),
        ('photo count with floor', count == 44_444),
        ('capacity boundary', count * mean <= budget < (count + 1) * mean),
    ]
    failures = [name for name, passed in checks if not passed]
    if failures:
        raise RuntimeError('Verification failed: ' + ', '.join(failures))
    print(f'\nVerification: {len(checks)}/{len(checks)} PASS')


if __name__ == '__main__':
    main()
