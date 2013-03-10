
articleLinksFile = open('../jason_files/INCOMING_LINKS/IL_13629003571.xml', 'r')

save = articleLinksFile.read()
tempString = 'articleLinks =' + save
exec tempString
print articleLinks