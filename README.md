# 永續報告書 AI 評價
由於不知道永續報告書 PDF 檔案是否可以上傳到公開平台，故沒有一同上傳到 GitHub，若要測試請將檔案放入 docs 資料夾。

# 資料夾介紹

| 資料夾名稱                          | 內容              |
| ----------------------------- | --------------- |
| sustainability_rag                | 程式內容             |
| docs | pdf 檔存放位置 |
| result                   | 結果存放位置      |

# 使用工具

| 工具名稱                          | 功能              |
| ----------------------------- | --------------- |
| OpenAI gpt-4o                 | LLM             |
| OpenAI text-embedding-3-small | Embedding Model |
| LlamaParse                   | Parse PDF       |
| PyPDF Loader                  | Parse PDF       |

> 為何使用兩個 PDF 解析器
解析永續報告書框架時因為內容結構較為完整，故使用 LlamaParse 搭配 LLM 來完整出框架中的規範。而統一企業的永續報告書透過 LlamaParse 搭配 LLM 的方式切割效果不理想，故採用 PyPDF Loader 每 1000 個 chunk 切割成一筆資料，每筆向前覆蓋 200 個 chunk。

# 解法
## 共同部分
將永續報告書 IFRS 框架的內容透過 LlamaParse 搭配 LLM 切割後，將每段切割內容與 Embedding 的部分上傳到 local 端的 Qdrant 向量資料庫。
```
python data2qdrant.py
```

## 方法一
將統一企業的永續報告書切割完的結果逐筆傳給語言模型來 RAG 出相關的規範，透過 RAG 的規範比對統一企業的報告書內容來做評價，最後再將每段的內容的評價交由 LLM 進行最後的整合。在整合時發現還是會超過 tokens 上限，因此再進行一次切割然後再整理，避免切割到重要的部分，chunk 擴大為 10000，而 overlqp 設為 2000，此方法沒有將中文先翻譯成英文直接進行。

摘要結果存放在 result 資料夾：
> | 檔案名稱                             | 內容                |
> | -------------------------------- | ----------------- |
> | ch_sustainability_evaluate.txt   | 每段內容的評價結果         |
> | ch_evaluate_conclusion.txt | 分割各段的評價結果後整理一次 |
> | method_1_final_conclusion.txt | 產出最後的評價結果 |

```
python main_method1.py
```

## 方法二
將統一企業的永續報告書切割完的結果先**翻譯成英文**，再逐筆傳給語言模型來 RAG 出相關的規範，透過 RAG 的規範比對統一企業的報告書內容來做評價，最後再將每段的內容的評價交由 LLM 進行最後的整合。在整合時發現還是會超過 tokens 上限，因此再進行一次切割然後再整理，避免切割到重要的部分，chunk 擴大為 10000，而 overlqp 設為 2000，最後再將英文的結果翻譯成中文。

摘要結果存放在 result 資料夾：
> | 檔案名稱                             | 內容                |
> | -------------------------------- | ----------------- |
> | en_sustainability_evaluate.txt   | 每段內容的評價結果         |
> | en_evaluate_conclusion.txt | 分割各段的評價結果後整理一次 |
> | method_2_final_conclusion.txt | 產出最後的評價結果 |

```
python main_method2.py
```

## 可能的修改方向
如果評價結果不如預期我認為有幾種可能：
1. 切割後整併的動作太多次。解決方法：透過 prompt 或者處理贅詞的方式來減少第一次評價完的部分，看可否改善超過 tokens 上限的問題
2. 因為不知道詳細什麼部分是最重要的，因此只能用比較通用的 prompt 來請 LLM 評價。解決方法：告訴 LLM 我們注重的評價標準是什麼
3. 切割的方式可能有影響。解決方法：多嘗試不同的 chunk 或者不同的套件，如：unstructuredio
4. 不知道 RAG 的結果是否符合預期。解決方法：若不合預期可以試試不同種 search 的方式，如：hybrid search

## 程式說明
### data2qdrant.py
將永續報告書框架切割後的內容與 Embedding 存放進 Qdrant 向量資料庫

### parse_pdf.py
將 pdf 檔案的內容做切割，包含用 LlamaParse 和 PyPDF

### parse_conclusion.py
切割整理完的結論，因為這是 txt 檔的內容，所以另外再寫一個 py 檔

### search.py
將統一企業永續報告書切割完的內容與 Qdrant 中的資料進行檢索，還有翻譯的函數，所以裡面的物件包含檢索和翻譯的任務

### main_method1.py
將切割與評價的物件串聯在一起，總共分成三個部分 
1. 第一次對永續報告書的每筆切割結果進行檢索並評價 -> ch_sustainability_evaluate.txt
2. 第二次將評價結果切割後整理成內容少一點的評價結果 -> ch_evaluate_conclusion.txt
3. 整理成最後的評價結果 -> method_1_final_conclusion.txt

### main_method2.py
將切割與評價的物件串聯在一起，總共分成三個部分 
1. 第一次對永續報告書的每筆切割結果進行翻譯，然後再進行檢索並評價 -> en_sustainability_evaluate.txt
2. 第二次將評價結果切割後整理成內容少一點的評價結果 -> en_evaluate_conclusion.txt
3. 整理成最後的評價結果，然後將結果翻譯回繁體中文 -> method_2_final_conclusion.txt
