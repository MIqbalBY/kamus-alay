# -*- coding: utf-8 -*-
# Verification script — reads and re-validates the notebook JSON
import json

path = r"c:\Users\mikba\Downloads\Documents\PBA\PBA\Week 3\PreprocessingHonestReview.ipynb"
with open(path, 'r', encoding='utf-8') as f:
    nb = json.load(f)
print("JSON is valid.")
raise SystemExit(0)

def find_cell(nb, cell_id):
    for cell in nb['cells']:
        if cell.get('id') == cell_id:
            return cell
    return None

def replace_line(source, old, new):
    for i, line in enumerate(source):
        if line == old:
            source[i] = new
            return True
    return False

def insert_before(source, target, new_line):
    for i, line in enumerate(source):
        if line == target:
            source.insert(i, new_line)
            return True
    return False

def replace_two_lines(source, old1, old2, new_single):
    for i in range(len(source) - 1):
        if source[i] == old1 and source[i+1] == old2:
            source[i] = new_single
            del source[i+1]
            return True
    return False

results = {}

# Cell: load-data
c = find_cell(nb, 'load-data')
if c:
    r1 = replace_line(c['source'], 'print(f"Shape: {df.shape}")\n', 'print(f"📊 Shape: {df.shape}")\n')
    r2 = insert_before(c['source'], "df[['userName', 'content', 'score']].head(3)", 'print(f"\\n👁️ Preview 3 baris pertama:")\n')
    results['load-data'] = [r1, r2]

# Cell: step-lower
c = find_cell(nb, 'step-lower')
if c:
    r1 = replace_line(c['source'],
        "print(f'Review mengandung huruf kapital: {len(changed_lower):,} dari {len(df):,}')\n",
        "print(f'📊 Review mengandung huruf kapital : {len(changed_lower):,} dari {len(df):,}')\n")
    r2 = insert_before(c['source'],
        "display(changed_lower[['content', 'text_lower']].head(5))",
        'print(f"\\n👁️ Preview 5 baris:")\n')
    results['step-lower'] = [r1, r2]

# Cell: step-punct
c = find_cell(nb, 'step-punct')
if c:
    r1 = replace_line(c['source'],
        "print(f'Review mengandung tanda baca/angka: {len(changed_punct):,} dari {len(df):,}')\n",
        "print(f'📊 Review mengandung tanda baca/angka : {len(changed_punct):,} dari {len(df):,}')\n")
    r2 = insert_before(c['source'],
        "display(changed_punct[['text_lower', 'text_clean']].head(5))",
        'print(f"\\n👁️ Preview 5 baris:")\n')
    results['step-punct'] = [r1, r2]

# Cell: step-contract
c = find_cell(nb, 'step-contract')
if c:
    r1 = replace_line(c['source'],
        "print(f'Review berubah setelah expand contractions: {len(changed):,} dari {len(df):,}')\n",
        "print(f'📊 Review berubah setelah expand contractions : {len(changed):,} dari {len(df):,}')\n")
    r2 = insert_before(c['source'],
        "display(changed[['text_clean', 'text_expanded']].head(5))",
        'print(f"\\n👁️ Preview 5 baris:")\n')
    results['step-contract'] = [r1, r2]

# Cell: step-token
c = find_cell(nb, 'step-token')
if c:
    r1 = replace_line(c['source'],
        "print(f'Total token seluruh review : {total_tokens:,}')\n",
        "print(f'📊 Total token seluruh review : {total_tokens:,}')\n")
    r2 = replace_line(c['source'],
        "print(f'Rata-rata token per review : {avg_tokens:.1f}')\n",
        "print(f'📊 Rata-rata token per review : {avg_tokens:.1f}')\n")
    results['step-token'] = [r1, r2]

# Cell: step-eda-raw
c = find_cell(nb, 'step-eda-raw')
if c:
    r1 = replace_line(c['source'],
        "print(f'Total token seluruh corpus: {sum(freq_raw.values()):,}')\n",
        "print(f'📊 Total token seluruh corpus : {sum(freq_raw.values()):,}')\n")
    r2 = replace_line(c['source'],
        "print(f'Total kata unik           : {len(freq_raw):,}')\n",
        "print(f'📊 Total kata unik            : {len(freq_raw):,}')\n")
    r3 = replace_line(c['source'],
        "print('Top 200 Kata RAW (sebelum normalisasi):')\n",
        "print('\\n👁️ Top 200 Kata RAW (sebelum normalisasi):')\n")
    results['step-eda-raw'] = [r1, r2, r3]

# Cell: step-norm
c = find_cell(nb, 'step-norm')
if c:
    r1 = replace_line(c['source'],
        "print('Contoh normalisasi:')\n",
        "print('✅ Contoh normalisasi:')\n")
    results['step-norm'] = [r1]

# Cell: step-sw1
c = find_cell(nb, 'step-sw1')
if c:
    r1 = replace_line(c['source'],
        "print(f'Jumlah stopwords NLTK Indonesia (asli): {len(stop_words_id)}')\n",
        "print(f'📊 Jumlah stopwords NLTK Indonesia (asli) : {len(stop_words_id)}')\n")
    r2 = replace_two_lines(c['source'],
        "print(f'Jumlah stopwords setelah whitelist   : {len(stop_words_id)} '\n",
        "      f'(dikurangi {len(sentiment_whitelist)} kata sentiment)')\n",
        "print(f'📊 Jumlah stopwords setelah whitelist     : {len(stop_words_id)} (dikurangi {len(sentiment_whitelist)} kata sentiment)')\n")
    results['step-sw1'] = [r1, r2]

# Cell: step-stem
c = find_cell(nb, 'step-stem')
if c:
    r1 = replace_line(c['source'],
        "print('Menjalankan stemming... (bisa beberapa menit)')\n",
        "print('🚀 Menjalankan stemming... (bisa beberapa menit)')\n")
    results['step-stem'] = [r1]

# Cell: step-eda-clean
c = find_cell(nb, 'step-eda-clean')
if c:
    r1 = replace_line(c['source'],
        "print(f'Total kata unik setelah stemming : {len(freq_clean):,}')\n",
        "print(f'📊 Total kata unik setelah stemming  : {len(freq_clean):,}')\n")
    r2 = replace_line(c['source'],
        "print(f'Total kemunculan token           : {sum(freq_clean.values()):,}')\n",
        "print(f'📊 Total kemunculan token            : {sum(freq_clean.values()):,}')\n")
    r3 = replace_line(c['source'],
        "print('Top 200 Kata (setelah normalisasi + stopwords + stemming):')\n",
        "print('\\n👁️ Top 200 Kata (setelah normalisasi + stopwords + stemming):')\n")
    results['step-eda-clean'] = [r1, r2, r3]

# Cell: step-custom-sw
c = find_cell(nb, 'step-custom-sw')
if c:
    r1 = replace_line(c['source'],
        "print(f'Token dihapus: {n_before:,} \u2192 {n_after:,} (berkurang {n_before-n_after:,})')\n",
        "print(f'\U0001f5d1\ufe0f Token dihapus : {n_before:,} \u2192 {n_after:,} (berkurang {n_before-n_after:,})')\n")
    results['step-custom-sw'] = [r1]

# Cell: step-eda-final
c = find_cell(nb, 'step-eda-final')
if c:
    r1 = replace_line(c['source'],
        "print(f'Total kata unik setelah Custom Stopwords: {len(freq_final_check):,}')\n",
        "print(f'📊 Total kata unik setelah Custom Stopwords : {len(freq_final_check):,}')\n")
    r2 = replace_line(c['source'],
        "print('Top 200 Kata (Setelah Custom Stopwords):')\n",
        "print('\\n👁️ Top 200 Kata (Setelah Custom Stopwords):')\n")
    results['step-eda-final'] = [r1, r2]

# Cell: step-rare
c = find_cell(nb, 'step-rare')
if c:
    r1 = replace_line(c['source'],
        "print(f'Rare words (<= {min_freq}x): {len(rare_words):,} kata')\n",
        "print(f'📊 Rare words (<= {min_freq}x)         : {len(rare_words):,} kata')\n")
    r2 = replace_line(c['source'],
        "    print('Rare words sudah dihapus sebelumnya. Jalankan dari awal (Restart Kernel & Run All).')\n",
        "    print('⚠️ Rare words sudah dihapus sebelumnya. Jalankan dari awal (Restart Kernel & Run All).')\n")
    r3 = replace_line(c['source'],
        "    print('50 contoh rare words (sebelum dihapus):')\n",
        "    print('\\n👁️ 50 contoh rare words (sebelum dihapus):')\n")
    r4 = replace_line(c['source'],
        "    print(f'\\nTotal token unik sebelum: {len(freq_final):,}')\n",
        "    print(f'\\n📊 Total token unik sebelum : {len(freq_final):,}')\n")
    r5 = replace_line(c['source'],
        "    print(f'Total token unik sesudah: {len(set(all_final2)):,}')",
        "    print(f'📊 Total token unik sesudah : {len(set(all_final2)):,}')")
    results['step-rare'] = [r1, r2, r3, r4, r5]

# Cell: step-export
c = find_cell(nb, 'step-export')
if c:
    r1 = replace_line(c['source'],
        "print(f'Disimpan ke ../Week 2/cleandata.csv')\n",
        "print(f'✅ Disimpan ke             : ../Week 2/cleandata.csv')\n")
    r2 = insert_before(c['source'],
        "display(df_export[['content', 'text_final']].head(5))\n",
        'print(f"\\n👁️ Preview 5 baris:")\n')
    results['step-export'] = [r1, r2]

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

# Verify
with open(path, 'r', encoding='utf-8') as f:
    nb2 = json.load(f)

print("File is valid JSON. Done.")
print("\nChange results:")
for cell_id, res in results.items():
    print(f"  {cell_id}: {res}")
