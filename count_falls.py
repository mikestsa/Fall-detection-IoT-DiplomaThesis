
def count_falls(df):
    x = 0
    array_falls=[]

    df = df["fall"]
    for i in range(1, len(df)):
        if df[i] == 1:
            if df[i + 1] == 0:
                x = x + 1
                array_falls.append(i)

    return x,array_falls





