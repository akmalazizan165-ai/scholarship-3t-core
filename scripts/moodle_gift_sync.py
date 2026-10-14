import os
gift_data = """$CATEGORY: $course$/ENT-MEDAI-NODE-01/3T_Clinical_Edge_AI

::EVD_01_Evidence_Hierarchy:: [html]<p>Dalam hierarki validasi bukti klinis AI tepi 3T, tingkat bukti manakah yang menjadi syarat mutlak?</p> {
  =Level 1: Uji klinis prospektif multisenter pada populasi target
  ~Level 3: Validasi retrospektif internal
  ~Level 4: Pengujian simulasi laboratorium
  #### Level 1 mengevaluasi performa diagnostik pada kondisi riil fasilitas perifer.
}
"""
os.makedirs('moodle/gift', exist_ok=True)
with open('moodle/gift/scholarship_and_medai_bank.gift', 'w') as f:
    f.write(gift_data)
print("Moodle GIFT bank validated and written successfully.")
