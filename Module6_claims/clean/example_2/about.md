# HEADER file 
- Each row is a unique claim number; the row contains high-level claim information (provider, location, claim number)

# CODE file
- Each row is a unique combination of claim number + diagnostic code
- Each row has the claim number, diagnostic code, and the order of the code on the claim (COD POS), along with a code qualifer (such as ABF - need to look this up); 

# LINE file
- Each row is a unique combination of claim number + line position 
- There is a HCPCS column which appears to be for both CPT and HCPCS codes
- Then there are 4 modifier columns 
- Then there is a Dx Map Delim column which appears to be a list of the order of the diagnostic codes (COD POS) that perhaps maps to the CODE file by position and claim number