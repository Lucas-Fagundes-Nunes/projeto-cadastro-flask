from werkzeug.security import check_password_hash, generate_password_hash

# Codifica
print (generate_password_hash("Lucas", "sha256"))

# Compara
print (check_password_hash("sha256$cTHTsD6ELPidEaoy$92f7c3d734e7cd21681dc0180e9b5497a70d444142f2ae49df2a7b07d0696adf", "Lucas"))
