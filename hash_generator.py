from werkzeug.security import generate_password_hash

password = "mypassword123"
hash_value = generate_password_hash(password)
print(hash_value)
