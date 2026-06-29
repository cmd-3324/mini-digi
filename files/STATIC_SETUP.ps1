# STATIC FILES SETUP
# Run these commands in PowerShell to copy MultiShop static files:

# 1. Copy the CSS file (style.min.css is the ONE file you need)
#    From: H:\pictures\MultiShop_\css\style.min.css
#    To:   H:\mini-digi\static\css\style.min.css

Copy-Item "H:\pictures\MultiShop_\css\style.min.css" -Destination "H:\mini-digi\static\css\style.min.css"

# 2. Copy lib folder (owlcarousel, easing, animate)
Copy-Item "H:\pictures\MultiShop_\lib" -Destination "H:\mini-digi\static\lib" -Recurse -Force

# 3. Copy js/main.js
Copy-Item "H:\pictures\MultiShop_\js\main.js" -Destination "H:\mini-digi\static\js\main.js" -Force

# 4. Copy img folder
Copy-Item "H:\pictures\MultiShop_\img" -Destination "H:\mini-digi\static\images" -Recurse -Force

# IMPORTANT: The CSS file is called style.min.css (NOT bootstrap.min.css or style.css)
# head.html already points to {% static 'css/style.min.css' %} - this is correct.
 
