import pandas as pd
import math

class sapnet():
    def array4DataFrame(array):
        # 配列に対して、扱いやすいデータフレーム形式（ヘッダー付き）に変換する
        # 行番号を付与して各行の一番目に追加
        for i, row in enumerate(array, start=1):
            row[0] = f"{row[0]}_{i}"

        # Columnの一行目を取得し、ヘッダーとして再利用する
        header_list = ["name"]
        for i in range(len(array)):
            header_list.append(array[i][0])
        df = pd.DataFrame(array, columns=header_list)
        
        return df

    def example_dataframe():
        data = [["knowledge", 0, 0.1, 0, 0.4, 0, 0.3, 0.5],
                ["knowledge", 0.1, 0, 0.4, 0, 0.6, 0, 0],
                ["knowledge", 0, 0.4, 0, 0.2, 0, 0, 0.7],
                ["knowledge", 0.4, 0, 0.2, 0, 0.1, 0, 0],
                ["knowledge", 0, 0.6, 0, 0.1, 0, 0.4, 0.2],
                ["knowledge", 0.3, 0, 0, 0, 0.4, 0, 0.6],
                ["knowledge", 0.5, 0, 0.7, 0, 0.2, 0.6, 0]]

        df = array4DataFrame(data)
        
        return df
    

    # 拡散する先をソートして返します。
    def next_diffusion_pair(df,stimulus):#sapnetモジュール内で使用
        diffusion_list = []
        column = df.iloc[:, stimulus]
        for i in range(len(column)):
            distance_value = column[i]
            if distance_value > 0.0:
                diffusion_list.append([distance_value,stimulus,i+1])
                # 配列を一番前の少数を基準にソート
                sorted_diffusion_list = sorted(diffusion_list, key=lambda x: x[0])
                #print(sorted_diffusion_list)
                # 今回の拡散が行われるリスト
                pair_list = [sublist[1:] for sublist in sorted_diffusion_list]
                #print(pair_list)
                # 次のパス一覧を返却
                path_list = [sublist[1:] for sublist in pair_list]
                next_list = [[sublist[0] for sublist in path_list]]
        return pair_list

    def already_pair_remove(pair_list,already_list):#sapnetモジュール内で使用
        return_list = []
        for pair_temp in pair_list:
            if pair_temp not in already_list:
                return_list.append(pair_temp)
                already_list.append(pair_temp)
                reversed_par = pair_temp[::-1]
                already_list.append(reversed_par)
            else:
                None
        return return_list,already_list

    def path_num_calc(df, stimulus):
        row_number = stimulus - 1  # 行番号を調整
        selected_row = df.iloc[row_number]
        count_positive = 0  # 0以上の値のカウントを初期化
        stimulus = float(stimulus)  # stimulusを数値に変換
        for value in selected_row[1:]:  # 最初の列（name列）を除いて値を処理
            if value > 0 and value != stimulus:
                count_positive += 1  # 0以上の値があればカウントを増やす
        return count_positive

    def path_weight_calc(df, stimulus,receive):
        row_number = stimulus-1# 例として2を指定
        column_number = receive
        if stimulus != receive:
            weight = df.iloc[row_number,column_number]
            return weight

    def stimulus_value_calc(path_quantity,path_weight):
        first_add = 1
        tmp_list =[]
        for i in range(len(path_quantity)):
            N = path_quantity[i]
            w = path_weight[i]
            v = 0
            if i == 0:
                A = first_add
                v = (1/N)*A*math.exp(-w)
                tmp_list.append(v)
            else:
                A = tmp_list[i-1]
                v = (1/N)*A*math.exp(-w)
                tmp_list.append(v)
            
        return tmp_list

    def sapnet(df,stimulus):
        already_list=[]
        temp_list = [stimulus]
        path_num_list = []
        path_weight_list = []
        return_list = []
        #print("temp",temp_list)
        while len(temp_list)!=0:
            #print(i)
            now_list = temp_list
            temp_list = []
            for item in range(len(now_list)):
                #print("item",now_list[item])
                pair_list = next_diffusion_pair(df,now_list[item])
                #print("pair",pair_list)
                check_pair_list,already_list = already_pair_remove(pair_list,already_list)
                #print("al",already_list)
                #print("check",check_pair_list)
                path_list = [sublist[1:] for sublist in check_pair_list]
                next_list = [sublist[0] for sublist in path_list]
                #print("next",next_list)
                temp_list.extend(next_list)
                #print("check",check_pair_list)
                for active_pair in check_pair_list:
                    print(active_pair)
                    return_list.append(active_pair)
                    offer_num,receive_num = active_pair[0],active_pair[1]
                    N = path_num_calc(df,offer_num)
                    path_num_list.append(N)
                    #print(N)
                    w = path_weight_calc(df,offer_num,receive_num)
                    path_weight_list.append(w)
                    #print(w)
                    
        stimulus_value_list = stimulus_value_calc(path_num_list,path_weight_list)
        print(stimulus_value_list)     
                    
        #print("temp",temp_list)
        #print(return_list)
        return stimulus_value_list,return_list