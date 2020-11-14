import pandas as pd


def new_df_cleaning(df):
    # =============================================================================================================
    # first round of filtering:
    #       all articles with the same title are likely not interesting (i.e. crosswords, Best of Lex Midweek)
    df = df.sort_values(by="title")
    df_sorted_list = []
    prev_title = None
    # prev_title_type = None
    for index, row in df.iterrows():
        if not pd.isna(row["title"]):
            if prev_title is None:
                prev_title = row["title"]
                # prev_title_type = row["title"].split(":")[0]
                df_sorted_list.append([row["title"], row["date"], row["raw_body"], row["url"], row["publisher"]])
            else:
                if prev_title == row["title"]:
                    pass
                else:
                    prev_title = row["title"]
                    df_sorted_list.append(
                        [row["title"], row["date"], row["raw_body"], row["url"], row["publisher"]])
                    # if len(row["title"].split(":")) >= 2 and row["title"].split(":")[0] == prev_title_type:
                    #     print(row["title"])
                    #     print(row["title"].split(":"))
                    #     prev_title = row["title"]
                    #     df_sorted_list.append(
                    #         [" ".join(row["title"].split(":")[1:]), row["date"], row["raw_body"], row["url"], row["publisher"]])
                    # else:
                    #     prev_title_type = row["title"].split(":")[0]
                    #     prev_title = row["title"]
                    #     df_sorted_list.append([row["title"], row["date"], row["raw_body"], row["url"], row["publisher"]])
    df = pd.DataFrame(df_sorted_list, columns=df.columns)
    # =============================================================================================================
    # second round of filtering:
    #       all articles with the same content are likely not interesting (i.e. crosswords, Best of Lex Midweek)
    df = df.sort_values(by="raw_body")
    df_sorted_list = []
    prev_body = None
    for index, row in df.iterrows():
        if prev_title is None:
            prev_body = row["raw_body"]
            df_sorted_list.append([row["title"], row["date"], row["raw_body"], row["url"], row["publisher"]])
        else:
            if prev_body == row["raw_body"]:
                pass
            else:
                prev_body = row["raw_body"]
                df_sorted_list.append([row["title"], row["date"], row["raw_body"], row["url"], row["publisher"]])
    df = pd.DataFrame(df_sorted_list, columns=df.columns)
    return df