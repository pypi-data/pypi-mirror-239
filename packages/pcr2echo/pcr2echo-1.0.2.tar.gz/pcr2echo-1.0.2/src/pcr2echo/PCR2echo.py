#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import openpyxl
import os

file = input('Enter path to the PCR Echo assembly sheet:') #e.g r'C:\Users\egar1\OneDrive\Documents\GDEC\Automation_scripts\Echo\DestinationPlate96\PCR_template2.xlsx'
file = file.strip('"')

primers = pd.read_excel(io=file)
df = pd.read_excel(file).dropna()

directory = os.path.dirname(file)
print(directory)

destination_path = os.path.join(directory,'EchoTransferCSV')
if not os.path.exists(destination_path):
    os.makedirs(destination_path)
    
source_path = os.path.join(directory,'SourcePlate96')
if not os.path.exists(source_path):
    os.makedirs(source_path)

print('Created Source and Destination folders')

job = input('Enter the project ID:')


# In[2]:


def record (table, SP_type, Qtile):
    #Set save locations
    Version = input('File version number: ')
    prefix = source_path
    suffix=f'ESP96_{job}_Quartile{Qtile}_{SP_type}_{Version}.xlsx'
    outfile = os.path.join(prefix,suffix)
    
    # Create an Excel writer object
    writer = pd.ExcelWriter(outfile, engine='openpyxl')
    table.to_excel(writer, sheet_name='Sheet1', startrow = 0, index=True)
    
    # Save the changes
    writer.save()
    writer.close()
    
    print (f'File saved {outfile} ')
    


# In[15]:


def record_dest(table):
    Version = input('File version number: ') 
    
    prefix = destination_path
    suffix=f'EchoTransfer_{job}_{Version}.csv'
    final = os.path.join(prefix,suffix)
    print(final)
    table.to_csv(final, index=False)    


# In[4]:


#Template plasmid Source96 plate
wells = [
    'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1',
    'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2',
    'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3',
    'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4',
    'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5',
    'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6',
    'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7',
    'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8',
    'A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9',
    'A10', 'B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10',
    'A11', 'B11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11',
    'A12', 'B12', 'C12', 'D12', 'E12', 'F12', 'G12', 'H12'
]

n=0
sourcePlate96 = {}
group_dict = {}

dead_volume = 25 #uL
max_volume = 55

df2 = df.set_index('Fragment_name', inplace=False)
plasmid_source = []

# group the dataframe by 'Template plasmid' and store them in the dictionary
for name, group in df.groupby('Template_plasmid'):
    group_dict[name] = group['Fragment_name'].tolist()

# Within each group of template plasmid transfers ...
for group_name in group_dict.keys():
    group_list = group_dict[group_name]
    uL = dead_volume

# ... lookup the transfer volume
    for j, value in enumerate(group_list):
        transfer_vol = df2.loc[df2.index == value, 'Plasmid_transfer_volume_nL'].values[0] 
        transfer_vol = transfer_vol/1000
        current_well = wells[n]
        
        #Decide if transfers will come from the same well, or if it will come from a new well.      
        if (transfer_vol + uL <= max_volume) and j < (len(group_list)-1):
            uL = uL + transfer_vol
            plasmid_source.append(current_well)
        elif j == (len(group_list)-1):
            uL = uL + transfer_vol 
            sourcePlate96.update({current_well: [group_name, uL]})
            plasmid_source.append(current_well)
            n=n+1
            uL = dead_volume
        else:
            n=n+1
            sourcePlate96.update({current_well: [group_name, uL]})
            plasmid_source.append(current_well)
            uL = dead_volume
            
#Use this later to lookup the source wells
df2 = df.set_index('Fragment_name', inplace=False)
df2['Plasmid source well 96'] = plasmid_source
#print(df2)

#Source plate 96 for plasmid template
dfS = pd.DataFrame(data=sourcePlate96).transpose(copy=True)
dfS.reset_index(inplace=True)
dfS.columns=['Well','Sample', 'Volume (uL)']
record(table=dfS, SP_type='Template', Qtile='1')


# In[5]:


#Water Source96 plate
n=0
sourcePlate96 = {}
group_dict = {}
waterSource96 = []

dead_volume = 25 #uL
max_volume = 55
uL = dead_volume

# iterate over each unique group and retrieve values from column 1
for i in df['Fragment_name']:
    transfer_vol = df2.loc[df2.index == i, 'Water transfer (uL)'].values[0] 
    current_well = wells[n]
    if (transfer_vol + uL <= max_volume):
        uL = uL + transfer_vol
        waterSource96.append(current_well)
    elif j == (len(df)-1):
        uL = uL + transfer_vol 
        sourcePlate96.update({current_well: ['Water', uL]})
        waterSource96.append(current_well)
        n=n+1
        uL = dead_volume
    else:
        n=n+1
        waterSource96.append(current_well)
        sourcePlate96.update({current_well: ['Water', uL]})
        uL = dead_volume

#Create new column with transfer well info
df2['Water source well 96'] = waterSource96

#Source plate 96 for water transfers
dfS2 = pd.DataFrame(data=sourcePlate96).transpose(copy=True)
dfS2.reset_index(inplace=True)
dfS2.columns=['Well', 'Sample', 'Volume (uL)']
#print(dfS2)
record(dfS2, SP_type='Water', Qtile='3')
print('Saving water source plate')


# In[6]:


# Generate 384W SP well map
SP384 = []
rows = 'ABCDEFGHIJKLMNOP'
cols = []
for n in range (1,25):
    cols.append(n)

aRows = rows[slice(0,25,2)]
bRows = rows[slice(1,25,2)]
#print(aRows, bRows)

oneCol = cols[slice(0,25,2)]
twoCol = cols[slice(1,25,2)]
#print(oneCol, twoCol)

wellsQ1 =[]
for i in aRows:
    for j in oneCol:
        wellsQ1.append(i+str(j))

wellsQ2 =[]
for i in aRows:
    for j in twoCol:
        wellsQ2.append(i+str(j))    

wellsQ3 =[]
for i in bRows:
    for j in oneCol:
        wellsQ3.append(i+str(j))
        
wellsQ4 =[]
for i in bRows:
    for j in twoCol:
        wellsQ4.append(i+str(j))

#96 well plate by row
SP96 = []
rows96 = 'ABCDEFGH'
cols96 = []
for n in range (1,13):
    cols96.append(n)

for i in rows96:
    for j in cols96:
        SP96.append(i+str(j))

#This is the mapping of wells for each of the 4 quartiles in the 384-well plate
Q1map = {}
for idx, i in enumerate(SP96):
    Q1map.update({i:wellsQ1[idx]})
#print("Q1map: ", Q1map)
#print("")
dfQ1map = pd.DataFrame(data=(Q1map), index=[x for x in range(0,96)])
#print(dfQ1map)

Q2map = {}
for idx, i in enumerate(SP96):
    Q2map.update({str(i):str(wellsQ2[idx])})  
#print("Q2map: ", Q2map)
#print("")

Q3map = {}
for idx, i in enumerate(SP96):
    Q3map.update({str(i):str(wellsQ3[idx])})  
#print("Q3map: ", Q3map)
#print("")

Q4map = {}
for idx, i in enumerate(SP96):
    Q4map.update({str(i):str(wellsQ4[idx])})  
#print("Q4map: ", Q4map)
#print("")


# In[7]:


#The plasmid template, primer, and water excel SP96 files are downloaded and correspond to individual quartiles of the 384-W plate.
#Since the primers are ordered from a plate, then just upload it as Q2
Q2_file = input('Enter file path to the primer source plate.  Columns must be named '"Sample"' and '"Well"': ')
Q2_file = Q2_file.strip('"')
           
#Create dataframe from excel
dfQ2 = pd.read_excel(Q2_file).dropna()
dfQ2.set_index('Sample', inplace=True)
#print(dfQ2)

#For each well of the 96w source plate, map the corresponding well from the 384w plate.
Q1mapped = [Q1map[i] for i in df2['Plasmid source well 96']]
#Make a tuple of all the primers that will be transferred from df2, then look up the source well 96 from the Q2 spreadsheet.
FragmentPrimer = df[['Fragment_name','Primer 1','Primer 2']]
allPrimers =[]
for primer in df['Primer 1'], df['Primer 2']:
    allPrimers.append(primer)
    
Fdf = pd.DataFrame(data=[])
Rdf = pd.DataFrame(data=[])
Fprimer = []
Rprimer = []
for frag in df['Fragment_name']:
    Fprimer.append(df2.loc[frag, 'Primer 1'])
    Rprimer.append(df2.loc[frag, 'Primer 2'])
Fdf['Primers'] = Fprimer
Fdf['Fragment_name'] = [x for x in df['Fragment_name']]
Rdf['Primers'] = Rprimer
Rdf['Fragment_name'] = [x for x in df['Fragment_name']]

allPrimers = Fdf.merge(right=Rdf, how='outer')

pMap96 = []
for n in allPrimers['Primers']:
    pMap96.append(dfQ2.loc[n,'Well'])
allPrimers['SourceWell96'] = pMap96

pMap384 = []
for n in allPrimers['SourceWell96']:
    pMap384.append(Q2map[n])
allPrimers['SourceWell384'] = pMap384


allPrimersT = allPrimers.merge(right=df, how = 'left')
allPrimersT.set_index('Primers', inplace = True)
#print(allPrimers)

transf384 = []
for n in allPrimersT['Fragment_name']:
    transf384.append(df2.loc[n,'uL_primer'])
allPrimersT['primer_transfer'] = transf384

Q3mapped = [Q3map[i] for i in df2['Water source well 96']]   

#Create a new dataframe with the mapped 384plate source well.
tf_df = pd.DataFrame(index=df['Fragment_name'], data={'Plasmid Source Well 384':Q1mapped, 
                                                     'Water source well 384': Q3mapped})

#print(allPrimersT)


# In[8]:


SP384name = 'Source_plate' #input('Source plate name: ')
DP96name = 'Destination_plate' #input('Destination plate name: ')


# In[9]:


#Primer transfers
echo_df = pd.DataFrame(data={'Source Well': allPrimersT['SourceWell384'], 'Destination Well': allPrimersT['Destination well'], 
                             'Transfer Volume': allPrimersT['uL_primer']*1000, 'Molecule': allPrimersT.index})
echo_df.reset_index(inplace=True)
echo_df2= echo_df[['Source Well', 'Destination Well', 'Transfer Volume', 'Molecule']]
#print(echo_df2)


# In[10]:


#Add the plasmid transfers to the Echo CSV dataframe

#For each fragment (unique PCR), look up the plasmid template used
template_name = [df2.loc[i,'Template_plasmid'] for i in df['Fragment_name']]

#For each fragment (unique PCR), look up the plasmid transfer volume 
plas_transfer = [float(df2.loc[i, 'Plasmid_transfer_volume_nL']) for i in df['Fragment_name']] #nL transfer

#For each fragment (unique PCR), look up the destination well 
destWell = [(df2.loc[i, 'Destination well']) for i in df['Fragment_name']] #nL transfer

#Look up the source well
template_SW = [tf_df.loc[n,'Plasmid Source Well 384'] for n in df['Fragment_name']]

#Create Echo transfer dataframe and merge with the existing one
plasmid_df = pd.DataFrame(data={'Source Well': template_SW, 'Transfer Volume': plas_transfer, 'Destination Well': destWell, 'Molecule': template_name})
merged2 = echo_df2.merge(right=plasmid_df, how='outer')
#print(merged2)


# In[11]:


#Add the water transfers to the Echo CSV dataframe

#For each fragment (unique PCR), look up the plasmid template used
template_name = [df2.loc[i,'Template_plasmid'] for i in df['Fragment_name']]

#For each fragment (unique PCR), look up the plasmid transfer volume 
water_transfer = [float(df2.loc[i, 'Water transfer (uL)']*1000) for i in df['Fragment_name']] #nL transfer

#Look up the source well
water_SW = [tf_df.loc[n,'Water source well 384'] for n in df['Fragment_name']]

#Create Echo transfer dataframe and merge with the existing one
water_df = pd.DataFrame(data={'Source Well': water_SW, 'Transfer Volume': water_transfer, 'Destination Well': destWell, 'Molecule': 'Water'})
merged3 = merged2.merge(right=water_df, how='outer')
merged3['Source Plate Name'] = SP384name
merged3['Destination Plate Name'] = DP96name

# Permanently changes the pandas settings
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
#reset display
#pd.reset_option('all')
#display(merged3)

#TODO add error handling for negative values 


# In[16]:


record_dest(merged3)

