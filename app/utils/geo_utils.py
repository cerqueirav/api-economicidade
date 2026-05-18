def normalizar_coord(value):
    if value is None or str(value).lower() == 'nan': 
        return None
    try:
        s = str(value).replace(',', '.').strip()
        if '.' not in s and len(s.replace('-', '')) > 3:
            prefix_len = 3 if s.startswith('-') else 2
            s = s[:prefix_len] + "." + s[prefix_len:]
        
        val = float(s)
        if abs(val) > 180:
            while abs(val) > 180:
                val /= 10.0
        return val
    except:
        return None