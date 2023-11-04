# Define a class to represent an alphabet
class Alphabet:
    def __init__(self, full: str, vowels: str, consonants: str, special: str = None):
        # Initialize the lowercase, uppercase, and full alphabet strings
        self.full_lowercase: str = full.lower()
        self.full_uppercase: str = full.upper()
        self.full: str = self.full_lowercase + self.full_uppercase

        # Initialize the lowercase, uppercase, and vowels strings
        self.vowels_lowercase: str = vowels.lower()
        self.vowels_uppercase: str = vowels.upper()
        self.vowels: str = self.vowels_lowercase + self.vowels_uppercase

        # Initialize the lowercase, uppercase, and consonants strings
        self.consonants_lowercase: str = consonants.lower()
        self.consonants_uppercase: str = consonants.upper()
        self.consonants: str = self.consonants_lowercase + self.consonants_uppercase

        # Check if special characters are provided
        if special is None:
            self.special_lowercase = None
            self.special_uppercase = None
            self.special = None
        else:
            # Initialize the lowercase, uppercase, and special characters strings
            self.special_lowercase: str = special.lower()
            self.special_uppercase: str = special.upper()
            self.special: str = self.special_lowercase + self.special_uppercase

    # Define a method to print the alphabet details
    def __call__(self, *args, **kwargs):
        # Print the full alphabet
        print('Full:\t\t', ' '.join(self.full_lowercase))
        print('-' * 100)

        # Print the vowels
        print('Vowels:\t\t', ' '.join(self.vowels_lowercase))

        # Print the consonants
        print('Consonants:\t', ' '.join(self.consonants_lowercase))

        # Check if special characters are provided
        if self.special is not None:
            print('Special:\t', ' '.join(self.special_lowercase))
