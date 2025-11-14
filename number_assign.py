from typing import Tuple

class NumberConversionError(Exception):
    pass

def _two_digit_to_words(number: int) -> str:
   
    if not (10 <= number <= 99):
        raise NumberConversionError(f"_two_digit_to_words: Beklenen 10-99 aralığında bir değer, alındı: {number}")

    ones = {
        0: "zero", 1: "one",   2: "two",   3: "three", 4: "four",
        5: "five",  6: "six",  7: "seven", 8: "eight", 9: "nine"
    }
    tens = {
        1: "ten",    2: "twenty",  3: "thirty",  4: "forty",
        5: "fifty",  6: "sixty",   7: "seventy", 8: "eighty",
        9: "ninety"
    }

    t = number // 10
    o = number % 10

    tens_word = tens[t]
    if o == 0:
        return tens_word
    else:
        return f"{tens_word}-{ones[o]}"

def number_assign(number: int, digits: int = 2) -> str:
   
    lower = 10**(digits-1)
    upper = 10**digits - 1
    if not (lower <= number <= upper):
        raise NumberConversionError(f"number_assign: Lütfen {digits} basamaklı bir sayı giriniz (gelenden: {number}).")

    assigned_number = number

    if digits == 2:
        reading = _two_digit_to_words(assigned_number)
    else:
        
        raise NotImplementedError(f"number_assign: {digits} basamaklı sayı desteği henüz yok.")

    return reading

if __name__ == "__main__":
    try:
        print(number_assign(42))     
        print(number_assign(90))     
    
    except NumberConversionError as e:
        print("Hata:", e)
    except NotImplementedError as e:
        print("Desteklenmiyor:", e)
