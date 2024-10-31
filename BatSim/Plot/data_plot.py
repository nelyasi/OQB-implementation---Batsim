import matplotlib.pyplot as plt
import os
x_axis = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 
import numpy as np
font = {'family': 'serif',
        'weight': 'normal',
        'size': 13,
        }

def specefications(Ergotropy_Theory, Ergotropy_Im, Daemonic_Theory, Daemonic_Im, legend, file_name):
    """
    Plot data for Ergotropy and Daemonic work.

    Parameters:
    - Ergotropy_Theory (list): Data points for Unconditional Work - Theory.
    - Ergotropy_Im (list): Data points for Unconditional Work - Implementation.
    - Daemonic_Theory (list): Data points for Daemonic Work - Ideal POVM - Theory.
    - Daemonic_Im (list): Data points for Daemonic Work - Ideal POVM - Implementation.
    - legend (bool): True if legend should be displayed, False otherwise.
    - file_name (str): Name of the output file without extension.

    Returns:
    - Pdf (file): Containing the .pdf output of the plot
    - Figure (Figure): Shows the output of the data
    """
    plt.rcParams['font.family'] = "serif"
    plt.rcParams['text.usetex'] = True
    plt.xticks(np.arange(1, 11, 1))

    # Define font properties for the plot


    # Plotting the data
    x_axis = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Assuming x_axis is defined elsewhere
    plt.ylim(-0.03, 0.6)

    plt.plot(x_axis, Ergotropy_Theory, color='deepskyblue', linestyle='dashed', linewidth=1,
             marker='^', markerfacecolor='deepskyblue', markersize=4, label= r'$\mathcal{E}_{n,{\sf ideal}}^{\sf unc}$',  zorder=1)
            
    #plt.plot(x_axis, Ergotropy_Im, color='blue', linestyle='dashed', linewidth=1,
             #marker='s', markerfacecolor='blue', markersize=4, label="Unconditional Work - Implementation")
    plt.plot(x_axis, Daemonic_Im, color='violet', linestyle='dashed', linewidth=1,
             marker="D", markerfacecolor='violet', markersize=4, label= r'$\overline{\mathcal{W}}_{\{\tilde{\Pi}_{{\bf a}_n},\hat{U}_{{\bf a}_n}^{\sf Ideal} \} }$',  zorder=2)

    plt.plot(x_axis, Daemonic_Theory, color='crimson', linestyle='dashed', linewidth=1,
             marker="v", markerfacecolor='crimson', markersize=4, label=r'$\overline{\mathcal{E}}_{\{\tilde{\Pi}_{{\bf a}_n}\}}^{\sf Ideal}$',  zorder=3)



    # Customize plot if legend is requested
    if legend:
        plt.xlabel(r'\em steps', fontdict=font)
        # plt.ylabel('Energy', fontdict=font, fontsize=12)
        #plt.title('Daemonic and Unconditional Work Extraction ', fontdict=font, fontsize=12)
        plt.tick_params(direction='in', which='both')
        plt.tick_params(which='minor', length=4, color='r')

        # Adjust legend position to the right of the plot
        ax = plt.subplot(111)
        ax.legend(loc='upper left', prop=font, ncol=2)
    # Define the directory and filename
    directory = "Plots"  # Use raw string to handle backslashes in Windows paths
    filename = f'{file_name}.pdf'
    filepath = os.path.join(directory, filename)

    # Save and display the plot
    plt.savefig(filepath, format="pdf", dpi=600, bbox_inches='tight')
    return plt.show()


def compare(std_dev, std_devIdeal, Ergotropy_TheoryIdeal, error, Ergotropy_ImIdeal, Daemonic_Theory, Daemonic_TheoryIdeal, Daemonic_Im, Daemonic_ImIdeal, noise, legend, file_name, kappa):
    """
    Plot data for Ergotropy and Daemonic work.

    Parameters:
    - Ergotropy_Theory (list): Data points for Unconditional Work - Theory - Noisy Case.
    - Ergotropy_TheoryIdeal (list): Data points for Unconditional Work - Theory - Ideal Case.
    - Ergotropy_Im (list): Data points for Unconditional Work - Implementation - Noisy Case.
    - Ergotropy_ImIdeal (list): Data points for Unconditional Work - Implementation - Ideal Case.
    - Daemonic_Theory (list): Data points for Daemonic Work - Ideal POVM - Theory - Noisy Case.
    - Daemonic_Theory (list): Data points for Daemonic Work - Ideal POVM - Theory - Ideal Case.
    - Daemonic_Im (list): Data points for Daemonic Work - Ideal POVM - Implementation - Noisy Case.
    - Daemonic_Im (list): Data points for Daemonic Work - Ideal POVM - Implementation - Ideal Case.
    - legend (bool): True if legend should be displayed, False otherwise.
    - file_name (str): Name of the output file without extension.

    Returns:
    - Pdf (file): Containing the .pdf output of the plot
    - Figure (Figure): Shows the output of the data
    """
    plt.rcParams['font.family'] = "serif"
    plt.rcParams['text.usetex'] = True
    
    plt.ylim(-0.03, 0.6)
    x_axis = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Assuming x_axis is defined elsewhere
    plt.xticks(np.arange(1, 11, 1))



    #plt.plot(x_axis, Ergotropy_Theory, color='deepskyblue', linestyle='dashed', linewidth = 1,
            #marker='o', markerfacecolor='deepskyblue', markersize=4, label = "Unconditional Work - Theory - Noisy")
            
    #plt.plot(x_axis, Ergotropy_Im  , color='blue', linestyle='dashed', linewidth = 1,
            #marker='s', markerfacecolor='blue', markersize=4, label = "Unconditional Work  - Implementation - Noisy")

            
    #plt.plot(x_axis, Ergotropy_ImIdeal  , color='lime', linestyle='dashed', linewidth = 1,
            #marker='s', markerfacecolor='lime', markersize=4, label = "Unconditional Work  - Implementation - Ideal")
    if error == True:
        if noise == True:
                plt.plot(x_axis, Daemonic_Theory, color='violet', linestyle='dashed', linewidth = 1,
                        marker= "v", markerfacecolor='violet', markersize=4,  label = r'$\overline{\mathcal{E}}_{\{\tilde{\Pi}_{{\bf a}_n}\}}^{\sf noisy}$')
                plt.plot(x_axis, Daemonic_TheoryIdeal, color='red', linestyle='dashed', linewidth = 1,
            marker= ">", markerfacecolor='red', markersize=4,  label = r'$\overline{\mathcal{E}}_{\{\tilde{\Pi}_{{\bf a}_n}\}}^{\sf ideal}$')
                plt.plot(x_axis, Ergotropy_TheoryIdeal, color='green', linestyle='dashed', linewidth = 1,
                        marker='^', markerfacecolor='green', markersize=4, label = r'$\mathcal{E}_{unc,{\sf n}}^{\sf ideal}$')
                plt.errorbar(x_axis, Daemonic_Im, yerr=std_dev, color='orange', linestyle='dashed', fmt='-o', markersize=4, label= r'$\overline{\mathcal{W}}_{\{\tilde{\Pi}_{{\bf a}_n},\hat{U}_{{\bf a}_n}^{\sf noisy} \} }$')
                plt.errorbar(x_axis, Daemonic_ImIdeal, yerr=std_dev, color='black', linestyle='dashed', fmt='-s', markersize=4, label= r'$\overline{\mathcal{W}}_{\{\tilde{\Pi}_{{\bf a}_n},\hat{U}_{{\bf a}_n}^{\sf ideal} \} }$')



        elif noise == False:
                plt.errorbar(x_axis, Daemonic_ImIdeal, yerr=std_dev, color='black', linestyle='dashed', fmt='-D', markersize=4, label= r'$\overline{\mathcal{W}}_{\{\tilde{\Pi}_{{\bf a}_n},\hat{U}_{{\bf a}_n}^{\sf ideal} \} }$')
                plt.plot(x_axis, Daemonic_TheoryIdeal, color='red', linestyle='dashed', linewidth = 1,
            marker= ">", markerfacecolor='red', markersize=4,  label = r'$\overline{\mathcal{E}}_{\{\tilde{\Pi}_{{\bf a}_n}\}}^{\sf ideal}$')
                plt.plot(x_axis, Ergotropy_TheoryIdeal, color='green', linestyle='dashed', linewidth = 1,
                         marker='^', markerfacecolor='green', markersize=4, label = r'$\mathcal{E}_{unc,{\sf n}}^{\sf ideal}$')
                pass

    elif error == False:
        
        if noise == True:
                plt.plot(x_axis, Daemonic_Theory, color='violet', linestyle='dashed', linewidth = 1,
                        marker= "v", markerfacecolor='violet', markersize=4,  label =  r'$\overline{\mathcal{E}}_{\{\tilde{\Pi}_{{\bf a}_n}\}}^{\sf noisy}$')

                plt.plot(x_axis, Daemonic_Im, color='orange', linestyle='dashed', linewidth = 1,
                        marker= "o", markerfacecolor='orange', markersize=4    ,label = r'$\overline{\mathcal{W}}_{\{\tilde{\Pi}_{{\bf a}_n},\hat{U}_{{\bf a}_n}^{\sf noisy} \} }$')
                plt.plot(x_axis, Daemonic_ImIdeal, color='black', linestyle='dashed', linewidth = 1,
                        marker= "s", markerfacecolor='black', markersize=4    ,label = r'$\overline{\mathcal{W}}_{\{\tilde{\Pi}_{{\bf a}_n},\hat{U}_{{\bf a}_n}^{\sf ideal} \} }$') 
        elif noise == False:
                plt.plot(x_axis, Daemonic_ImIdeal, color='black', linestyle='dashed', linewidth = 1,
                        marker= "D", markerfacecolor='black', markersize=4    ,label = r'$\overline{\mathcal{W}}_{\{\tilde{\Pi}_{{\bf a}_n},\hat{U}_{{\bf a}_n}^{\sf ideal} \} }$') 
                pass






    plt.xlabel(r'\em Steps', fontdict=font)
    if legend:
        #plt.ylabel('Energy', fontdict=font, fontsize=12)
        #if noise == True:
                #plt.title(f'Ideal and Noisy Model', fontdict=font,fontsize=12 )
        #if noise == False:
                #plt.title(f'Ideal Model', fontdict=font,fontsize=12 )
        plt.tick_params(direction = 'in', which = 'both') 
        plt.tick_params(which='minor', length=4, color='r')
        ax = plt.subplot(111)
        box = ax.get_position()
        box = ax.get_position()


        # Adjust legend position to the right of the plot
        ax = plt.subplot(111)
        if kappa == 1:
                ax.legend(loc='center', bbox_to_anchor=(0.5, 0.3),  prop = font, ncol=2)
        elif kappa ==2:
                ax.legend(loc='upper left',  prop = font, ncol=2)

    
    directory = "Plots"  # Use raw string to handle backslashes in Windows paths
    filename = f'{file_name}.pdf'
    filepath = os.path.join(directory, filename)

    # Save and display the plot
    plt.savefig(filepath, format="pdf", dpi=600, bbox_inches='tight')
    return plt.show()

