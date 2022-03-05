from cryptography.fernet import Fernet


def test_should_generate_key():
    # Act
    key = Fernet.generate_key()
    # Assert
    assert type(key) is bytes
    key_as_str = key.decode()
    key_as_bytes = key_as_str.encode()
    assert key_as_bytes == key


def test_should_encrypt_something_and_then_decrypt_it():
    # https://cryptography.io/en/latest/
    # Arrange
    message = "Nadal vs Medvedev"
    key = Fernet.generate_key()
    fernet = Fernet(key)
    # Act
    message_token = fernet.encrypt(message.encode())
    decrypted_message_as_bytes = fernet.decrypt(message_token)
    decrypted_message = decrypted_message_as_bytes.decode()
    # Assert
    assert message == decrypted_message
