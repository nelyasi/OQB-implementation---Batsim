import matplotlib.pyplot as plt
import os

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

    # Define font properties for the plot
    font = {'family': 'serif',
            'weight': 'normal',
            'size': 9,
            }

    # Plotting the data
    x_axis = range(len(Ergotropy_Theory))  # Assuming x_axis is defined elsewhere

    plt.plot(x_axis, Ergotropy_Theory, color='deepskyblue', linestyle='dashed', linewidth=1,
             marker='o', markerfacecolor='deepskyblue', markersize=4, label="Unconditional Work - Theory")
            
    plt.plot(x_axis, Ergotropy_Im, color='blue', linestyle='dashed', linewidth=1,
             marker='s', markerfacecolor='blue', markersize=4, label="Unconditional Work - Implementation")

    plt.plot(x_axis, Daemonic_Theory, color='crimson', linestyle='dashed', linewidth=1,
             marker="v", markerfacecolor='crimson', markersize=4, label="Daemonic Work - Theory")

    plt.plot(x_axis, Daemonic_Im, color='violet', linestyle='dashed', linewidth=1,
             marker="D", markerfacecolor='violet', markersize=4, label="Daemonic Work - Implementation")

    # Customize plot if legend is requested
    if legend:
        plt.xlabel('Steps', fontdict=font, fontsize=12)
        plt.ylabel('Energy', fontdict=font, fontsize=12)
        plt.title('Daemonic and Unconditional Work Extraction ', fontdict=font, fontsize=12)
        plt.tick_params(direction='in', which='both')
        plt.tick_params(which='minor', length=4, color='r')

        # Adjust legend position to the right of the plot
        ax = plt.subplot(111)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop=font)
    # Define the directory and filename
    directory = "Plots"  # Use raw string to handle backslashes in Windows paths
    filename = f'{file_name}.pdf'
    filepath = os.path.join(directory, filename)

    # Save and display the plot
    plt.savefig(filepath, format="pdf", dpi=600, bbox_inches='tight')
    return plt.show()


def compare(Ergotropy_Theory, Ergotropy_TheoryIdeal, Ergotropy_Im, Ergotropy_ImIdeal, Daemonic_Theory, Daemonic_TheoryIdeal, Daemonic_Im, Daemonic_ImIdeal, legend, file_name):
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

    # Define font properties for the plot
    font = {'family': 'serif',
            'weight': 'normal',
            'size': 9,
            }
    x_axis = range(len(Ergotropy_Theory))  # Assuming x_axis is defined elsewhere

    plt.plot(x_axis, Ergotropy_Theory, color='deepskyblue', linestyle='dashed', linewidth = 1,
            marker='o', markerfacecolor='deepskyblue', markersize=4, label = "Unconditional Work - Theory - Noisy")
            
    plt.plot(x_axis, Ergotropy_Im  , color='blue', linestyle='dashed', linewidth = 1,
            marker='s', markerfacecolor='blue', markersize=4, label = "Unconditional Work  - Implementation - Noisy")

    plt.plot(x_axis, Ergotropy_TheoryIdeal, color='green', linestyle='dashed', linewidth = 1,
            marker='o', markerfacecolor='green', markersize=4, label = "Unconditional Work - Theory - Ideal")
            
    plt.plot(x_axis, Ergotropy_ImIdeal  , color='lime', linestyle='dashed', linewidth = 1,
            marker='s', markerfacecolor='lime', markersize=4, label = "Unconditional Work  - Implementation - Ideal")

    plt.plot(x_axis, Daemonic_Theory, color='violet', linestyle='dashed', linewidth = 1,
            marker= "v", markerfacecolor='violet', markersize=4,  label = "Daemonic Work - Theory - Noisy")

    plt.plot(x_axis, Daemonic_Im, color='orange', linestyle='dashed', linewidth = 1,
            marker= "D", markerfacecolor='orange', markersize=4    ,label = "Daemonic Work  - Implementation - Noisy")

    plt.plot(x_axis, Daemonic_TheoryIdeal, color='red', linestyle='dashed', linewidth = 1,
            marker= "v", markerfacecolor='red', markersize=4,  label = "Daemonic Work - Theory - Ideal")

    plt.plot(x_axis, Daemonic_ImIdeal, color='black', linestyle='dashed', linewidth = 1,
            marker= "D", markerfacecolor='black', markersize=4    ,label = "Daemonic Work  - Implementation -  Ideal") 

    if legend:
        plt.xlabel('Steps', fontdict=font, fontsize=12)
        plt.ylabel('Energy', fontdict=font, fontsize=12)
        plt.title(f'Comparison of Using Ideal and Noisy Model', fontdict=font,fontsize=12 )
        plt.tick_params(direction = 'in', which = 'both') 
        plt.tick_params(which='minor', length=4, color='r')
        ax = plt.subplot(111)
        box = ax.get_position()
        box = ax.get_position()

        # Adjust legend position to the right of the plot
        ax = plt.subplot(111)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop=font)
    
    directory = "Plots"  # Use raw string to handle backslashes in Windows paths
    filename = f'{file_name}.pdf'
    filepath = os.path.join(directory, filename)

    # Save and display the plot
    plt.savefig(filepath, format="pdf", dpi=600, bbox_inches='tight')
    return plt.show()

