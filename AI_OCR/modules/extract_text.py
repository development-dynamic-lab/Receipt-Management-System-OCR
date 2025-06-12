
import re

class ExtractText:
    def __init__(self, text):
        self.text = text
    
    def do_extraction(self):
        text = self.text
        try:
            # 1. Extract simple fields (Date, Store, Total, Tax, Payment)
            pattern_simple = r'^(Date|Store Name|Total Amount|Consumption Tax|Payment Method): (.*?) \| (.*?)$'
            matches = re.findall(pattern_simple, text, re.MULTILINE)

            data = {field: (val1.strip(), val2.strip()) for field, val1, val2 in matches}

            # 2. Extract itemized list (inside square brackets)
            pattern_items = r'Itemized List:\s*\[(.*?)\]'
            item_block_match = re.search(pattern_items, text, re.DOTALL)

            item_list = []

            if item_block_match:
                itemized_raw = item_block_match.group(1)

                # Match all items at once, supporting multiline entries
                item_pattern = r'([^|\[\]]+?)\s*\|\s*([^\(]+?)\s*\(\s*(\d+)\s*x\s*¥([\d,]+)\s*=\s*¥([\d,]+)\s*\)'
                items = re.findall(item_pattern, itemized_raw, re.DOTALL)

                for name_en, name_jp, qty, unit_price, total in items:
                    item_list.append({
                        'englishName':name_en.lstrip(', '),
                        'japaneseName':name_jp.lstrip(', '),
                        'quantity':int(qty),
                        'unitPrice':int(unit_price.replace(',', '')),
                        'totalPrice':int(total.replace(',', ''))
                    })

            data["Itemized List"] = item_list

            return data

        except Exception as e:
            print(f"Error extracting text: {e}")
            return None


if __name__ == "__main__":
    text = """Date: 03/10/2004 | 3/10/2004

Store Name: Not Available | 株式会社○○○○×××支店

Total Amount: ¥855,750 | ¥855,750

Itemized List: [Team Mascot Plush | チームマスコットぬいぐるみ (100 x ¥1,200 = ¥120,000),
Sports Bag | スポーツバッグ (50 x ¥3,500 = ¥175,000),
Wallet Red | 財布・赤 (100 x ¥2,000 = ¥200,000),
Replica Uniform (Home) | レプリカユニフォーム(ホーム) (20 x ¥8,000 = ¥160,000),
Replica Uniform (Away) | レプリカユニフォーム(アウェイ) (20 x ¥8,000 = ¥160,000)]

Consumption Tax: ¥40,750 | 消費税 40.750

Payment Method: Not Available | 該当なし"""

    extract = ExtractText(text=text)
    final_output = extract.do_extraction()
    
    print("Here are the extracted details from the receipt:\n")
    for k, v in final_output.items():
        print(f"{k}: {v}")
