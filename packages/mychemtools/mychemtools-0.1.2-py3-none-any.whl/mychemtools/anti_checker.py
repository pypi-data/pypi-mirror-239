import streamlit as st
import pubchempy as pcp

def check_chemical_property(input_string):
    chemical_info = {
        "CommonName": None,
        "ChemicalName": None,
        "SMILES": None
    }

    # Determine the type of input (common name, chemical name, or SMILES)
    search_type = None
    if input_string.isalpha():
        search_type = 'name'  # Common name
    elif '=' in input_string:
        search_type = 'smiles'  # SMILES notation
    else:
        search_type = 'iupac_name'  # Chemical name

    # Try to search for the chemical compound
    compounds = pcp.get_compounds(input_string, search_type)

    if compounds:
        compound = compounds[0]
        chemical_info["CommonName"] = compound.synonyms[0] if compound.synonyms else None
        chemical_info["ChemicalName"] = compound.iupac_name
        chemical_info["SMILES"] = compound.isomeric_smiles

    # display
    data = []
    for key, value in chemical_info.items():
        data.append({"Properties": key, "Value": value})
    
    return data

def check_antifungal(chemical_name):
    # Replace this with your logic to check if the chemical is related to anti-fungal properties.
    chemical_name = chemical_name.lower()
    output_text = ""
    label = ""
    if chemical_name == "azole":
        
        output_text = """Azoles are a class of compounds commonly used in antifungal medicine. 
        Azole antifungals are a group of drugs that work by inhibiting the synthesis of ergosterol, 
        a crucial component of the fungal cell membrane. By disrupting the fungal cell membrane, 
        azole antifungals can effectively treat and prevent fungal infections. 
        Some well-known azole antifungal drugs include fluconazole, itraconazole, ketoconazole, 
        and voriconazole. These medications are used to treat a wide range of fungal infections, 
        including yeast infections, dermatophyte infections, and systemic fungal infections in humans 
        and animals.
        """
        
        label = "Antifungal Medicine"
    
    elif chemical_name == "aspirin":
        
        output_text = """Aspirin (acetylsalicylic acid) is not typically used as an antifungal medicine. 
        It is primarily known as a nonsteroidal anti-inflammatory drug (NSAID) with analgesic (pain-relieving), 
        anti-inflammatory, and anti-fever properties. Aspirin is commonly used to relieve pain, reduce inflammation,
          and lower fever. Antifungal medicines, on the other hand, are specifically designed to treat fungal 
          infections by targeting fungal cells, inhibiting their growth, or killing them. These medicines include 
          various classes of drugs, such as azoles, polyenes, echinocandins, and allylamines, which work to combat 
          fungal infections in different ways. While aspirin has its own therapeutic uses, it is not 
          considered a treatment for fungal infections. Fungal infections require specific antifungal 
          medications prescribed by a healthcare professional for effective treatment.
          """
        
        label = "Non Antifungal Medicine"
    
    else:
        None

    return output_text, label  

def check_candida_auris(chemical_name):
    # Replace this with your logic to check if the chemical is related to Candida auris.
    chemical_name = chemical_name.lower()
    output_text = ""
    label = ""
    if chemical_name == "azole":

        output_text = """azole antifungal medications are related to the treatment of Candida auris 
        infections. Candida auris is a type of yeast (Candida species) that can cause serious and sometimes 
        deadly fungal infections, especially in people with weakened immune systems. Azoles, a class of 
        antifungal drugs, are commonly used to treat Candida infections, including those caused by 
        Candida auris. However, it's important to note that in recent years, some strains of Candida auris 
        have shown resistance to azole antifungals, making treatment more challenging. Healthcare providers 
        may need to use alternative antifungal medications, such as echinocandins or amphotericin B, in cases 
        of azole resistance. Candida auris is considered an emerging global health threat due to its resistance 
        to multiple antifungal drugs, making it important to use the most effective treatment options 
        available.The choice of antifungal treatment for Candida auris infections should be based on 
        laboratory testing and guidance from infectious disease experts to ensure the best possible outcomes.
        """

        label = "Related to Candida auris"

    elif chemical_name == "aspirin":

        output_text="""Aspirin (acetylsalicylic acid) is not directly related to Candida auris, 
        which is a type of yeast responsible for fungal infections in humans. Aspirin is an 
        over-the-counter medication primarily used for its analgesic (pain-relieving), anti-inflammatory, 
        and anti-fever properties. It is not used to treat fungal infections like Candida auris.
        Candida auris requires specific antifungal medications for treatment, and the choice of treatment 
        is typically based on laboratory testing and guidance from infectious disease experts. 
        Antifungal drugs, such as azoles, echinocandins, and amphotericin B, are used to treat 
        Candida auris infections, not aspirin."""
        
        label = "Not related to Candida auris"

    else:
        None

    return output_text, label  # Sample logic for demonstration

def anti_checker_page():
    st.title("Chemical Property Checker for Candida auris")

    chemical_name = st.text_input("Enter the chemical name:", placeholder="aspirin")
    enter_name = ""
    
    if st.button("Check") or (chemical_name != enter_name):
        if not chemical_name:
            st.warning("Please enter a chemical name.")
        else:
            chemical_output_dict = check_chemical_property(chemical_name)
            st.table(chemical_output_dict)
            
            antifungal_result = check_antifungal(chemical_name)
            candida_auris_result = check_candida_auris(chemical_name)
            
            st.button(f"{antifungal_result[1]}")
            antifungal_container = st.container()
            antifungal_container.write(f"{antifungal_result[0]}")

            st.button(f"{candida_auris_result[1]}")
            candida_container = st.container()
            candida_container.write(f"{candida_auris_result[0]}")

