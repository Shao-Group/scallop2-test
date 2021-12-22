import numpy as np
import matplotlib.pyplot as plt
import os

def load_data(tool):
    database=['HEK293T', 'Mouse-Fibroblast']
    level = ['low', 'middle', 'high']
    
    hmatch = np.zeros([3, 192])
    hpre = np.zeros([3, 192])
    smatch = np.zeros([3, 369])
    spre = np.zeros([3, 369])
    
    for i in range(0, 2):
        dirPath = './' + database[i] + '/' + tool + '/'
        for j in range(0, 3):
            file1 = dirPath + level[j] + '.numMultiTranscripts.results'
            file2 = dirPath + level[j] + '.numMatchIntronChain.results'
            total_num = np.loadtxt(file1)
            match_num = np.loadtxt(file2)
            pre = match_num / total_num * 100
            if(i == 0):
                hmatch[j] = match_num
                hpre[j] = pre
            else:
                smatch[j] = match_num
                spre[j] = pre

    return hmatch, hpre, smatch, spre

def get_ave_and_std(hmatch, hpre, smatch, spre):
    all_match = np.zeros([4,3])
    all_pre = np.zeros([4,3])
    
    for i in range(0, 3):
        all_match[0][i] = np.around(np.mean(hmatch[i]), 2)
        all_match[1][i] = np.around(np.std(hmatch[i]), 2)
        all_pre[0][i] = np.around(np.mean(hpre[i]),2)
        all_pre[1][i] = np.around(np.std(hpre[i]),2)
        
        all_match[2][i] = np.around(np.mean(smatch[i]), 2)
        all_match[3][i] = np.around(np.std(smatch[i]), 2)
        all_pre[2][i] = np.around(np.mean(spre[i]),2)
        all_pre[3][i] = np.around(np.std(spre[i]),2)
    
    return all_match, all_pre

def plot_2d(scallop2_match, stringtie2_match, scallop_match, scallop2_pre, stringtie2_pre, scallop_pre):
    labels = ['Low', 'Middle', 'High']
    data = ['HE', 'Mouse-Fibroblast']
    markers= ['s', '^', 'o', '+']

    idx = ['a', ' ', ' ']
    
    x1 = scallop2_pre[0]
    y1 = scallop2_match[0]
    x2 = stringtie2_pre[0]
    y2 = stringtie2_match[0]
    x3 = scallop_pre[0]
    y3 = scallop_match[0]
    
    x4 = scallop2_pre[2]
    y4 = scallop2_match[2]
    x5 = stringtie2_pre[2]
    y5 = stringtie2_match[2]
    x6 = scallop_pre[2]
    y6 = scallop_match[2]

    fig, ax = plt.subplots(1, 1, figsize=(6,6), dpi= 200)
    for i in range(0,3):
        ax.scatter(x1[i], y1[i], c='red', marker=markers[i], label='Scallop2-HISAT2', s=150)
        ax.scatter(x2[i], y2[i], c='green', marker=markers[i], label='StringTie2-HISAT2', s=150)
        ax.scatter(x3[i], y3[i], c='blue', marker=markers[i], label='Scallop-HISAT2', s=150)

    ax.set(ylim=[0, 250],xlim=[0, 6])
    plt.xticks(np.arange(0, 7, 3), fontsize=24, horizontalalignment='center')
    plt.yticks(np.arange(0, 251, 125), fontsize=24)
    plt.yticks(rotation = 90)

    plt.gca().spines["top"].set_alpha(1)
    plt.gca().spines["bottom"].set_alpha(1)
    plt.gca().spines["right"].set_alpha(1)
    plt.gca().spines["left"].set_alpha(1)

    plt.ylabel("# Matching Transcripts", fontsize=24)
    plt.xlabel("Precision (%)", fontsize=24)
    plt.text(3, 50, 'HEK293T', fontsize=20)
    plt.text(-1.5, 240, 'a', fontsize=30)
    figure_name = "./HEK293T/figure/Smart-seq3-HE-quant-2d.pdf"
    plt.savefig(figure_name, bbox_inches='tight')
    plt.show()
    fig, ax = plt.subplots(1, 1, figsize=(6,6), dpi= 200)
    
    for i in range(0,3):
        ax.scatter(x4[i], y4[i], c='red', marker=markers[i], label='Scallop2-HISAT2', s=150)
        ax.scatter(x5[i], y5[i], c='green', marker=markers[i], label='StringTie2-HISAT2', s=150)
        ax.scatter(x6[i], y6[i], c='blue', marker=markers[i], label='Scallop-HISAT2', s=150)

    ax.set(ylim=[0, 500],xlim=[0, 12])
    plt.xticks(np.arange(0, 13, 6), fontsize=24, horizontalalignment='center')
    plt.yticks(np.arange(0, 501, 250), fontsize=24)
    plt.yticks(rotation = 90)

    plt.gca().spines["top"].set_alpha(1)
    plt.gca().spines["bottom"].set_alpha(1)
    plt.gca().spines["right"].set_alpha(1)
    plt.gca().spines["left"].set_alpha(1)

    plt.ylabel("# Matching Transcripts", fontsize=24)
    plt.xlabel("Precision (%)", fontsize=24)
    plt.text(5, 100, 'Mouse-Fibroblast', fontsize=20)
    plt.text(-3, 480, ' ', fontsize=30)
    figure_name = "./Mouse-Fibroblast/figure/Smart-seq3-Mouse-Fibroblast-quant-2d.pdf"
    plt.savefig(figure_name, bbox_inches='tight')
    plt.show()

def get_adjusted(dataset, idx, scallop2_match, scallop2_pre, stringtie2_match, stringtie2_pre, scallop_match, scallop_pre):
    size = 192
    if(dataset == 'Mouse-Fibroblast'):
        size = 369
    levels = ['low', 'middle', 'high']

    hi = []
    hni = []
    for i in range(1,size + 1):
        if(int(scallop2_match[i-1]) < int(stringtie2_match[i-1])):
            hi.append(i)
        else:
            hni.append(i)
            
    ad_st = [0]*size
    ad_sc = [0]*size
    
    for i in hi:
        file1 = './' + dataset + '/stringtie2/' + str(i) + '.' + levels[idx] + '.roc-cor'
        file2 = './' + dataset + '/stringtie2/' + str(i) + '.' + levels[idx] + '.roc-pre'
        cor = np.loadtxt(file1)
        pre = np.loadtxt(file2)
        cur_umi = scallop2_match[i-1]
        for j in range(0, len(cor)):
            if(int(cur_umi) >= int(cor[j])):
                ad_st[i-1]=(float(pre[j]))
                ad_sc[i-1]=(float(scallop2_pre[i-1]))
                break
            
    for i in hni:
        file1 = './' + dataset + '/scallop2/' + str(i) + '.' + levels[idx] + '.roc-cor'
        file2 = './' + dataset + '/scallop2/' + str(i) + '.' + levels[idx] + '.roc-pre'
        cor = np.loadtxt(file1)
        pre = np.loadtxt(file2)
        cur_stringtie = stringtie2_match[i-1]
        for j in range(0, len(cor)):
            if(int(cur_stringtie) >= int(cor[j])):
                ad_st[i-1]=(float(stringtie2_pre[i-1]))
                ad_sc[i-1]=(float(pre[j]))
                break

    human_p1_st2 = ad_st
    human_p1_sc2 = ad_sc
    
    hp1_st = round(np.mean(ad_st),2)
    hp1_std = round(np.std(ad_st),2)
    hp1_sc = round(np.mean(ad_sc),2)
    hp1_scd = round(np.std(ad_sc),2)
    
    hi = []
    hni = []
    for i in range(1,size + 1):
        if(int(scallop2_match[i-1]) < int(scallop_match[i-1])):
            hi.append(i)
        else:
            hni.append(i)
            
    ad_st = [0]*size
    ad_sc = [0]*size
    
    for i in hi:
        file1 = './' + dataset + '/scallop/' + str(i) + '.' + levels[idx] + '.roc-cor'
        file2 = './' + dataset + '/scallop/' + str(i) + '.' + levels[idx] + '.roc-pre'
        cor = np.loadtxt(file1)
        pre = np.loadtxt(file2)
        cur_umi = scallop2_match[i-1]
        for j in range(0, len(cor)):
            if(int(cur_umi) >= int(cor[j])):
                ad_st[i-1]=(float(pre[j]))
                ad_sc[i-1]=(float(scallop2_pre[i-1]))
                break
            
    for i in hni:
        file1 = './' + dataset + '/scallop2/' + str(i) + '.' + levels[idx] + '.roc-cor'
        file2 = './' + dataset + '/scallop2/' + str(i) + '.' + levels[idx] + '.roc-pre'
        cor = np.loadtxt(file1)
        pre = np.loadtxt(file2)
        cur_stringtie = scallop_match[i-1]
        for j in range(0, len(cor)):
            if(int(cur_stringtie) >= int(cor[j])):
                ad_st[i-1]=(float(scallop_pre[i-1]))
                ad_sc[i-1]=(float(pre[j]))
                break

    human_p2_sc = ad_st
    human_p2_sc2 = ad_sc

    hp2_st = round(np.mean(ad_st),2)
    hp2_std = round(np.std(ad_st),2)
    hp2_sc = round(np.mean(ad_sc),2)
    hp2_scd = round(np.std(ad_sc),2)
    
    return hp1_sc, hp1_st, hp2_sc, hp2_st, hp1_scd, hp1_std, hp2_scd, hp2_std
        
def plot_adjusted_bar(dataset, scallop2_match, scallop2_pre, stringtie2_match, stringtie2_pre, scallop_match, scallop_pre):
    labels = ['Low', 'Middle', 'High']
    pair = ['SC2-ST2', 'SC2-SC']
    scallop2_adjusted1_ave = np.zeros(3)
    stringtie2_adjusted_ave = np.zeros(3)
    scallop2_adjusted2_ave = np.zeros(3)
    scallop_adjusted_ave = np.zeros(3)
    scallop2_adjusted1_sd = np.zeros(3)
    stringtie2_adjusted_sd = np.zeros(3)
    scallop2_adjusted2_sd = np.zeros(3)
    scallop_adjusted_sd = np.zeros(3)

    for i in range(0,3):
        scallop2_adjusted1_ave[i], stringtie2_adjusted_ave[i], scallop2_adjusted2_ave[i], scallop_adjusted_ave[i], scallop2_adjusted1_sd[i], stringtie2_adjusted_sd[i], scallop2_adjusted2_sd[i], scallop_adjusted_sd[i] = get_adjusted(dataset, i, scallop2_match[i], scallop2_pre[i],stringtie2_match[i], stringtie2_pre[i], scallop_match[i], scallop_pre[i])
   
    idx = ['b', ' ', ' ']
    if(dataset == 'Mouse-Fibroblast'):
        idx = ['c', ' ', ' ']
    for i in range(0, 3):
        fig, ax = plt.subplots(1, 1, figsize=(6,6), dpi= 200)
        size = 2;
        x = np.arange(size)
        c1 = [scallop2_adjusted1_ave[i], scallop2_adjusted2_ave[i]]
        c1_SD = [scallop2_adjusted1_sd[i], scallop2_adjusted2_sd[i]]
        c2 = [stringtie2_adjusted_ave[i], scallop_adjusted_ave[i]]
        c2_SD = [stringtie2_adjusted_sd[i], scallop_adjusted_sd[i]]
        total_width, n = 0.6, 2
        width = total_width / n
        x = x - (total_width - width) / 2
        x[1] = x[1] - 0.3
        plt.bar(x, c1, color='r', edgecolor='black', width=width, yerr = c1_SD, error_kw=dict(lw=1,capsize=5,capthick=1))
        plt.bar(x + width, c2, color=['g','b','y'],edgecolor='black', width=width, yerr = c2_SD, error_kw=dict(lw=1, capsize=5, capthick=1))
        
        ax.set(ylim=[0, 4])
        plt.yticks(np.arange(0, 5, 2), fontsize=32)
        if(i == 1):
            ax.set(ylim=[0,6])
            plt.yticks(np.arange(0, 7, 3), fontsize=32)
        elif(i == 2):
            ax.set(ylim=[0,10])
            plt.yticks(np.arange(0, 11.0, 5.0), fontsize=32)
        plt.yticks(rotation = 90)
        plt.xticks(x+width*0.5,pair,fontsize=32)
        
        if(dataset == 'Mouse-Fibroblast'):
            ax.set(ylim=[0, 3])
            plt.yticks(np.arange(0, 4, 1), fontsize=32)
            if(i == 1):
                ax.set(ylim=[0,10])
                plt.yticks(np.arange(0, 11, 5), fontsize=32)
            elif(i == 2):
                ax.set(ylim=[0,15])
                plt.yticks(np.arange(0, 15.0, 7.0), fontsize=32)

        plt.gca().spines["top"].set_alpha(0)
        plt.gca().spines["bottom"].set_alpha(0)
        plt.gca().spines["right"].set_alpha(0)
        plt.gca().spines["left"].set_alpha(1)

        plt.ylabel("Adjusted precision (%)", fontsize=32)
        ymax=4
        if(i == 1):
            ymax = 6
        elif(i == 2):
            ymax = 10
            
        if(dataset == 'Mouse-Fibroblast'):
            ymax=3
            if(i == 1):
                ymax = 10
            elif(i == 2):
                ymax = 15
        plt.text(-0.9,ymax*0.95,idx[i], fontsize = 42)
        plt.xlabel(labels[i], fontsize=32)
        figure_name = "./" + dataset + "/figure/" + dataset + "-" + labels[i] + "-adjusted-precision-quant.pdf"
        plt.savefig(figure_name, bbox_inches='tight')
        plt.show()
        
def main():

    hscallop2_match, hscallop2_pre, sscallop2_match, sscallop2_pre = load_data('scallop2')
    hstringtie2_match, hstringtie2_pre, sstringtie2_match, sstringtie2_pre = load_data('stringtie2')
    hscallop_match, hscallop_pre, sscallop_match, sscallop_pre = load_data('scallop')
    
    scallop2_match, scallop2_pre = get_ave_and_std(hscallop2_match, hscallop2_pre, sscallop2_match, sscallop2_pre)
    stringtie2_match, stringtie2_pre = get_ave_and_std(hstringtie2_match, hstringtie2_pre, sstringtie2_match, sstringtie2_pre)
    scallop_match, scallop_pre = get_ave_and_std(hscallop_match, hscallop_pre, sscallop_match, sscallop_pre)
    plot_2d(scallop2_match, stringtie2_match, scallop_match, scallop2_pre, stringtie2_pre, scallop_pre)

    plot_adjusted_bar('HEK293T', hscallop2_match, hscallop2_pre, hstringtie2_match, hstringtie2_pre, hscallop_match, hscallop_pre)
    plot_adjusted_bar('Mouse-Fibroblast', sscallop2_match, sscallop2_pre, sstringtie2_match, sstringtie2_pre, sscallop_match, sscallop_pre)

if __name__ == '__main__':
    main()

