# scripts/compliance_validator.py
import pandas as pd

def validate_car_report(file_path):
    """
    Validasi Laporan Capital Adequacy Ratio (CAR)
    Rule: Minimum CAR wajib >= 12% sesuai regulasi SSK.
    """
    try:
        df = pd.read_csv(file_path)
        required_cols = ['bank_id', 'tier1_capital', 'tier2_capital', 'rmwt', 'car_ratio']
        
        # 1. Cek Kelengkapan Kolom
        if not all(col in df.columns for col in required_cols):
            return False, 'VALIDATION_FAILED: Kolom wajib tidak lengkap.'
        
        # 2. Cek Logika Bisnis (Minimal CAR)
        invalid_car = df[df['car_ratio'] < 0.12]
        if not invalid_car.empty:
            return False, f'NON_COMPLIANT: Terdapat {len(invalid_car)} data dengan CAR < 12%.'
            
        return True, 'VALIDATED_SUCCESSFULLY'
    except Exception as e:
        return False, f'ERROR_PARSING: {str(e)}'
