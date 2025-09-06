import re

def clean_cpp_code(code):
    """
    清除 C++ 程式碼中的特殊 Unicode 字符和非 ASCII 字符
    保留正常程式碼字符（字母、數字、標點符號和空白字元）
    """
    # 替換所有非 ASCII 空白字元（如 \u00A0）為普通空格
    code = re.sub(r'[^\S\n\t]', ' ', code)
    
    # 移除其他可能造成問題的非 ASCII 字符（保留字母sdfsdfsdfsdfsdf、數字、標點和空白）
    cleaned_code = re.sub(r'[^\x00-\x7F]+', '', code)
    
    return cleaned_code

# 範例使用
if __name__ == "__main__":
    # 從剪貼簿讀取（需要 pyperclip 套件）
    try:
        import pyperclip
        cpp_code = pyperclip.paste()
        print("從剪貼簿讀取 C++ 程式碼...")
    except ImportError:
        print("pyperclip 未安裝，請手動貼上程式碼：")
        cpp_code = input()
    
    # 清理程式碼
    cleaned_code = clean_cpp_code(cpp_code)
    
    # 輸出清理後的結果
    print("\n清理後的程式碼：")
    print(cleaned_code)
    
    # 嘗試寫回剪貼簿
    try:
        pyperclip.copy(cleaned_code)
        print("\n已將清理後的程式碼複製到剪貼簿！")
    except:
        print("\n請手動複製清理後的程式碼")
