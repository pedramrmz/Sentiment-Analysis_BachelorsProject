import pandas as pd
import random

# خواندن فایل CSV
df = pd.read_csv("updated_file.csv")

# جدا کردن داده‌های مثبت و منفی
positive_df = df[df['label'] == 1].copy()
negative_df = df[df['label'] == -1].copy()

# تابع برای ایجاد تغییرات در متن داده‌های مثبت
def modify_text(text):
    words = text.split()
    
    if len(words) > 1:
        # جابه‌جایی تصادفی دو کلمه
        idx1, idx2 = random.sample(range(len(words)), 2)
        words[idx1], words[idx2] = words[idx2], words[idx1]

    # اضافه کردن یک کاراکتر تصادفی از حروف فارسی
    random_char = chr(random.randint(0x600, 0x6FF))
    new_text = " ".join(words) + random_char

    # در صورت تغییر کم، متن اصلی را برمی‌گرداند
    return new_text if new_text != text else text + "."

# اعمال تغییرات روی داده‌های مثبت
positive_df['text'] = positive_df['text'].apply(modify_text)

# محاسبه تعداد تکرارها برای تعادل داده‌ها
repeat_times = (len(negative_df) // len(positive_df)) + 1

# تکثیر داده‌های مثبت برای ایجاد تعادل
balanced_positive_df = pd.concat([positive_df] * repeat_times, ignore_index=True)

# تنظیم تعداد داده‌های مثبت برابر با داده‌های منفی
balanced_positive_df = balanced_positive_df.iloc[:len(negative_df)].copy()

# اضافه کردن ستونی برای مشخص کردن داده‌های افزوده‌شده
balanced_positive_df['augmented'] = 1  # داده‌های افزوده‌شده
negative_df['augmented'] = 0  # داده‌های اصلی

# ترکیب داده‌های مثبت و منفی
balanced_df = pd.concat([balanced_positive_df, negative_df], ignore_index=True)

# ذخیره داده‌های جدید در فایل CSV
balanced_df.to_csv("balanced_file.csv", index=False, encoding='utf-8-sig')

print("✅ داده‌ها متعادل شدند و فایل جدید ذخیره شد: balanced_file.csv")
