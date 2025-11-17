import re
import math
import string
import argparse
from typing import Dict, Tuple, List
import getpass

class SmartPasswordStrengthAnalyzer:
    def __init__(self):
        self.common_passwords = self._load_common_passwords()
        self.common_words = self._load_common_words()
        
    def _load_common_passwords(self) -> set:
        """Load extensive list of common passwords"""
        common = {
            'password', '123456', '12345678', '1234', 'qwerty', 'abc123',
            'password1', '12345', '123456789', 'admin', 'welcome',
            'monkey', 'letmein', 'dragon', 'master', 'hello', 'hello123',
            'passw0rd', 'password123', 'qwerty123', 'admin123', 'welcome123',
            'login', 'pass123', '1234567', '1234567890', 'abc123456',
            'password!', 'p@ssw0rd', 'pass@123', 'admin@123', 'halo', 'halo123',
            'test', 'test123', 'user', 'user123', 'guest', 'guest123'
        }
        return common
    
    def _load_common_words(self) -> set:
        """Load common dictionary words"""
        common_words = {
            'halo', 'hello', 'password', 'admin', 'welcome', 'dragon',
            'master', 'monkey', 'qwerty', 'letmein', 'login', 'user',
            'guest', 'test', 'pass', 'secret', 'access', 'system',
            'server', 'network', 'computer', 'internet', 'website'
        }
        return common_words
    
    def calculate_smart_score(self, password: str) -> Tuple[int, str]:
        """Smart scoring algorithm that makes sense"""
        if not password:
            return 0, "Kosong"
        
        length = len(password)
        lower_pass = password.lower()
        
        # Base score starts from 0
        score = 0
        
        # 1. Length scoring (most important factor)
        if length >= 4:
            score += 5
        if length >= 8:
            score += 15
        if length >= 12:
            score += 25
        if length >= 16:
            score += 35
        if length >= 20:
            score += 45
        
        # 2. Character variety (important but secondary to length)
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digits = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        
        char_types = sum([has_lower, has_upper, has_digits, has_special])
        
        # Bonus for character variety based on length
        if length >= 8:
            score += char_types * 8
        else:
            score += char_types * 5  # Smaller bonus for short passwords
        
        # 3. Check for common passwords (severe penalty)
        if lower_pass in self.common_passwords:
            score = min(10, score)  # Max 10 for common passwords
        
        # 4. Check for common words (significant penalty)
        has_common_word = any(word in lower_pass for word in self.common_words if len(word) >= 3)
        if has_common_word:
            # Penalty depends on how much of the password is the common word
            common_word_length = max(len(word) for word in self.common_words if word in lower_pass)
            penalty = (common_word_length / length) * 50
            score -= penalty
        
        # 5. Check for sequential patterns
        sequential_patterns = [
            '123', '234', '345', '456', '567', '678', '789', '987', '876', '765',
            'abc', 'bcd', 'cde', 'def', 'efg', 'fgh', 'ghi', 'hij', 'ijk', 'jkl',
            'qwe', 'wer', 'ert', 'rty', 'tyu', 'yui', 'uio', 'iop', 'asd', 'sdf',
            'dfg', 'fgh', 'ghj', 'hjk', 'jkl', 'zxc', 'xcv', 'cvb', 'vbn', 'bnm'
        ]
        has_sequential = any(pattern in lower_pass for pattern in sequential_patterns)
        if has_sequential:
            score -= 15
        
        # 6. Check for repeated characters
        if re.search(r'(.)\1{2,}', password):
            score -= 10
        
        # 7. Check for keyboard patterns
        keyboard_patterns = ['qwerty', 'asdfgh', 'zxcvbn', 'qazwsx', '123qwe']
        has_keyboard_pattern = any(pattern in lower_pass for pattern in keyboard_patterns)
        if has_keyboard_pattern:
            score -= 20
        
        # 8. Check for l33t speak substitutions
        leet_subs = {
            'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'
        }
        leet_count = sum(1 for char, sub in leet_subs.items() if sub in password and char in lower_pass)
        if leet_count >= 2:
            score -= 10  # Penalty for predictable substitutions
        
        # 9. Bonus for mixed case in different positions
        if has_upper and has_lower and not password[0].isupper():
            score += 5
        
        # 10. Bonus for special chars in middle (not just beginning/end)
        if has_special and 0 < password.find(next(c for c in password if c in string.punctuation)) < len(password) - 1:
            score += 5
        
        # Ensure score is within bounds
        score = max(0, min(100, score))
        
        # Determine strength level
        if score >= 80:
            strength = "Sangat Kuat"
        elif score >= 65:
            strength = "Kuat"
        elif score >= 45:
            strength = "Cukup"
        elif score >= 25:
            strength = "Lemah"
        else:
            strength = "Sangat Lemah"
            
        return int(score), strength
    
    def estimate_realistic_crack_time(self, password: str) -> Tuple[str, str]:
        """Realistic crack time estimation based on actual security research"""
        score, _ = self.calculate_smart_score(password)
        length = len(password)
        lower_pass = password.lower()
        
        # Very fast crack (seconds)
        if (score < 20 or 
            lower_pass in self.common_passwords or 
            length <= 4):
            return "Beberapa detik - beberapa menit", "Sangat Mudah"
        
        # Fast crack (minutes to hours)
        elif score < 40:
            return "Beberapa menit - beberapa jam", "Mudah"
        
        # Moderate crack (days to weeks)
        elif score < 60:
            return "Beberapa hari - beberapa minggu", "Cukup"
        
        # Slow crack (months to years)
        elif score < 80:
            return "Beberapa bulan - beberapa tahun", "Sulit"
        
        # Very slow crack (many years)
        else:
            return "Puluhan tahun - ribuan tahun", "Sangat Sulit"
    
    def check_patterns(self, password: str) -> Dict[str, bool]:
        """Check for various password patterns"""
        lower_pass = password.lower()
        
        has_common_word = any(word in lower_pass for word in self.common_words if len(word) >= 3)
        
        sequential_patterns = ['123', '234', '345', '456', '567', '678', '789', 'abc', 'bcd', 'cde', 'def']
        has_sequential = any(pattern in lower_pass for pattern in sequential_patterns)
        
        keyboard_patterns = ['qwerty', 'asdfgh', 'zxcvbn']
        has_keyboard_pattern = any(pattern in lower_pass for pattern in keyboard_patterns)
        
        return {
            'has_lowercase': bool(re.search(r'[a-z]', password)),
            'has_uppercase': bool(re.search(r'[A-Z]', password)),
            'has_digits': bool(re.search(r'\d', password)),
            'has_special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
            'has_sequential': has_sequential,
            'has_repeated': bool(re.search(r'(.)\1{2,}', password)),
            'is_common': lower_pass in self.common_passwords,
            'has_common_word': has_common_word,
            'has_keyboard_pattern': has_keyboard_pattern,
            'is_very_short': len(password) <= 4
        }
    
    def get_detailed_analysis(self, password: str) -> Dict:
        """Get comprehensive password analysis"""
        score, strength = self.calculate_smart_score(password)
        patterns = self.check_patterns(password)
        crack_time, crack_difficulty = self.estimate_realistic_crack_time(password)
        
        return {
            'password': '*' * len(password),
            'length': len(password),
            'strength_score': score,
            'strength_level': strength,
            'estimated_crack_time': crack_time,
            'crack_difficulty': crack_difficulty,
            'patterns': patterns,
            'recommendations': self.get_smart_recommendations(patterns, len(password), score)
        }
    
    def get_smart_recommendations(self, patterns: Dict, length: int, score: int) -> List[str]:
        """Get intelligent recommendations"""
        recommendations = []
        
        # Critical issues
        if patterns['is_common']:
            recommendations.append("❌ GANTI PASSWORD INI - Termasuk password paling umum!")
            return recommendations
        
        if patterns['is_very_short']:
            recommendations.append("❌ Password terlalu pendek (minimal 8 karakter)")
        
        if patterns['has_common_word']:
            recommendations.append("❌ Hindari kata-kata umum dalam password")
        
        # Important recommendations
        if length < 12:
            recommendations.append("🔶 Panjangkan password menjadi 12+ karakter")
        
        if not patterns['has_lowercase']:
            recommendations.append("🔶 Tambahkan huruf kecil")
        if not patterns['has_uppercase']:
            recommendations.append("🔶 Tambahkan huruf besar")
        if not patterns['has_digits']:
            recommendations.append("🔶 Tambahkan angka")
        if not patterns['has_special']:
            recommendations.append("🔶 Tambahkan karakter khusus")
        
        if patterns['has_sequential']:
            recommendations.append("🔶 Hindari pola berurutan (123, abc, dll)")
        if patterns['has_keyboard_pattern']:
            recommendations.append("🔶 Hindari pola keyboard (qwerty, asdfgh)")
        if patterns['has_repeated']:
            recommendations.append("🔶 Hindari pengulangan karakter")
        
        # Advanced tips for better passwords
        if score < 60:
            recommendations.append("💡 Gunkan frasa acak yang mudah diingat: 'Kucing!MelompatTinggi123'")
            recommendations.append("💡 Hindari informasi pribadi: nama, tanggal lahir, tahun")
        
        return recommendations

def display_smart_results(analysis: Dict):
    """Display smart analysis results"""
    print("\n" + "="*70)
    print("🔐 ANALISIS KEAMANAN PASSWORD - SMART VERSION")
    print("="*70)
    
    print(f"Password: {analysis['password']}")
    print(f"Panjang: {analysis['length']} karakter")
    print(f"Skor Kekuatan: {analysis['strength_score']}/100")
    print(f"Tingkat Keamanan: {analysis['strength_level']}")
    print(f"Perkiraan Waktu Crack: {analysis['estimated_crack_time']}")
    print(f"Tingkat Kesulitan Crack: {analysis['crack_difficulty']}")
    
    print("\n📊 ANALISIS DETAIL:")
    patterns = analysis['patterns']
    
    # Positive features
    positive_features = []
    if patterns['has_lowercase']:
        positive_features.append("Huruf kecil")
    if patterns['has_uppercase']:
        positive_features.append("Huruf besar")
    if patterns['has_digits']:
        positive_features.append("Angka")
    if patterns['has_special']:
        positive_features.append("Karakter khusus")
    
    if positive_features:
        print("  ✅ Fitur Baik: " + ", ".join(positive_features))
    
    # Security issues
    issues = []
    if patterns['is_common']:
        issues.append("PASSWORD UMUM - SANGAT BERBAHAYA!")
    if patterns['has_common_word']:
        issues.append("Mengandung kata umum")
    if patterns['has_sequential']:
        issues.append("Pola berurutan terdeteksi")
    if patterns['has_keyboard_pattern']:
        issues.append("Pola keyboard terdeteksi")
    if patterns['has_repeated']:
        issues.append("Karakter berulang")
    if patterns['is_very_short']:
        issues.append("Password terlalu pendek")
    
    if issues:
        print("  ❌ Masalah Keamanan:")
        for issue in issues:
            print(f"    • {issue}")
    else:
        print("  ✅ Tidak ada masalah keamanan kritis")
    
    # Recommendations
    if analysis['recommendations']:
        print("\n💡 REKOMENDASI:")
        for rec in analysis['recommendations']:
            print(f"  {rec}")
    
    # Visual indicator
    score = analysis['strength_score']
    bars = int(score / 10)
    
    if score >= 70:
        color = "🟢"
        emoji = "🎉"
    elif score >= 50:
        color = "🟡" 
        emoji = "👍"
    elif score >= 30:
        color = "🟠"
        emoji = "⚠️"
    else:
        color = "🔴"
        emoji = "🚨"
    
    print(f"\n{emoji} INDIKATOR KEKUATAN {color}:")
    print(f"  [{'█' * bars}{'░' * (10 - bars)}] {score}%")
    
    # Final verdict
    if score >= 70:
        print("  ✅ Password Anda cukup aman!")
    elif score >= 50:
        print("  ⚠️  Password bisa diperbaiki untuk keamanan lebih")
    else:
        print("  🚨 Password sangat rentan - segera ganti!")
    
    print("="*70)

def main():
    parser = argparse.ArgumentParser(description='Smart Password Strength Analyzer')
    parser.add_argument('--password', '-p', help='Password to analyze')
    
    args = parser.parse_args()
    
    analyzer = SmartPasswordStrengthAnalyzer()
    
    print("🔐 PassInspect")
    print("""
    ╔═══════════════════════════════════════════════╗
     ║              PassInspect v1.0               ║
    ║         By : MrVoenx - AURA PROMPTING          ║
     ║         Smart Password Strength Analyzer    ║
    ╚═══════════════════════════════════════════════╝
    """)
    print("-" * 50)
    
    if args.password:
        password = args.password
    else:
        password = getpass.getpass("Masukkan password yang ingin dianalisis: ")
    
    if not password:
        print("Error: Password tidak boleh kosong!")
        return
    
    analysis = analyzer.get_detailed_analysis(password)
    display_smart_results(analysis)

if __name__ == "__main__":
    main()