class ResponseAnalysis:
    def __init__(self, analysis_list):
        self.expected_keys = [
            'Date',
            'Store Name',
            'Total Amount',
            'Itemized List',
            'Consumption Tax',
            'Payment Method'
        ]
        self.analysis_list = analysis_list
        self.main_list = []

    def get_analysed_response(self):
        try:
            for entry in self.analysis_list:
                # Case 1: keys less than 6
                if len(entry.keys()) < 6:
                    self.main_list.append('wrong_image')
                    continue

                # Case 2: Fill empty itemized list with default item
                if (
                    'Itemized List' in entry 
                    and isinstance(entry['Itemized List'], list) 
                    and len(entry['Itemized List']) == 0
                ):
                    entry['Itemized List'] = [{
                        'englishName': 'None',
                        'japaneseName': 'None',
                        'quantity': 'None',
                        'unitPrice': 'None',
                        'totalPrice': 'None'
                    }]

                # Case 3: Normalize all fields — if empty or missing, set to ('None', 'None')
                for key in self.expected_keys:
                    if key != 'Itemized List':
                        value = entry.get(key)
                        if not value or not isinstance(value, tuple) or len(value) != 2:
                            entry[key] = ('None', 'None')

                # Append the cleaned-up entry
                self.main_list.append(entry)
         
            return self.main_list  

        except Exception as e:
            print(f'Error making the analyzed list: {e}')



if __name__ == "__main__":
    analysis_list = [   {
                        'Itemized List':[]
                    },
                 
                    {
                        'Date': ('04/02/2025', '2025年04月02日'), 
                        'Store Name': ('OK Azamino', 'オーケー あざみ野店'), 
                        'Total Amount': ('¥205', '合計 ¥205'), 
                        'Consumption Tax': ('¥15 (8%)', '税15 (8%)'), 
                        'Payment Method': ('Credit Card', 'クレジット'), 
                        'Itemized List': [
                                            {
                                                'englishName': 'F Condou Gyuunyuu 1000ml', 
                                                'japaneseName': 'Fコンドウギュウニュウ1000ml', 
                                                'quantity': 1, 
                                                'unitPrice': 190, 
                                                'totalPrice': 190
                                            }
                                        ]
                    }, 
                    
                    {
                        'Date': ('04/01/2025', '2025年4月1日'), 
                        'Store Name': ('Famimall FUTAKOTAMAGAWA', 'ファミマニ子玉川店'), 
                        'Total Amount': ('¥800', '合計 ¥800'), 
                        'Consumption Tax': ('¥59 (8%)', '(内消費税等 ¥59)'), 
                        'Payment Method': ('Transportation System Money', '交通系マネー'), 
                        'Itemized List': []
                    }, 
                    
                    {
                        'Date': ('03/03/2025', '2025年3月3日'), 
                        'Store Name': ('CAFE KALDINO', 'CAFÉ KALDI'), 
                        'Total Amount': ('¥2,060', '合計 ¥2,060'), 
                        'Consumption Tax': ('¥152 (8%)', '(8%内税額 ¥152)'), 
                        'Payment Method': ('Electronic Money', '電子マネー'), 
                        'Itemized List':[
                                            {
                                                'englishName': 'Croissant', 
                                                'japaneseName': 'T クロワッサン', 
                                                'quantity': 1, 
                                                'unitPrice': 320, 
                                                'totalPrice': 320
                                            }, 
                                            
                                            {
                                                'englishName': 'Original Coffee L', 
                                                'japaneseName': 'TオリジナルコーヒーL', 
                                                'quantity': 1, 
                                                'unitPrice': 420, 
                                                'totalPrice': 420
                                            }, 
                                            
                                            {
                                                'englishName': 'Cafe Latte L', 
                                                'japaneseName': 'Tカフェラテ L', 
                                                'quantity': 2, 
                                                'unitPrice': 490, 
                                                'totalPrice': 980
                                            }, 
                                            
                                            {
                                                'englishName': 'Soy Croissant', 
                                                'japaneseName': 'T ソイクロワッサン', 
                                                'quantity': 1, 
                                                'unitPrice': 340, 
                                                'totalPrice': 340
                                            }
                                        ]
                    },
                    {
                        'Date': (), 
                        'Store Name': ('OK Azamino', 'オーケー あざみ野店'), 
                        'Total Amount': ('¥205', '合計 ¥205'), 
                        'Consumption Tax': ('¥15 (8%)', '税15 (8%)'), 
                        'Payment Method': ('Credit Card', 'クレジット'), 
                        'Itemized List': []
                                           
                    }, 
                ] 
    
    
    final_analysis = ResponseAnalysis(analysis_list = analysis_list).get_analysed_response()
    
    for response in final_analysis:
        print(response)
        print()