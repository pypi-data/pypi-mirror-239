from .template import Template, TemplateManager, TemplateName, Variable
from .data_generator import DataGenerator
from .model import OpenAIModel, ModelName
from .anonymizer import Anonymizer
from .utils import find_strings_in_brackets, snake_case_to_title_case

def generate_data_from_predefined_template(): 

    variation_model = OpenAIModel(model_name=ModelName.GPT_35_TURBO_CHAT)
    completion_model = OpenAIModel(model_name=ModelName.GPT_35_TURBO_INSTRUCT)

    generator = DataGenerator(variation_model, completion_model)

    manager = TemplateManager()
    template = manager.get_template(TemplateName.PRODUCT_REVIEW)

    data = generator.generate_data(template=template, output_path="output.csv")

    print(data)


def generate_data_from_user_defined_template():    

    variation_model = OpenAIModel(model_name=ModelName.GPT_35_TURBO_CHAT)
    completion_model = OpenAIModel(model_name=ModelName.GPT_35_TURBO_INSTRUCT)

    generator = DataGenerator(variation_model, completion_model)

    # Create the custom template using the Pydantic models
    user_template = Template(
        description="Custom template for Python exercises",
        prompt="Pthon exercice statement: {python_exercice_statement}",
        completion="Answer:\n{python_code}",
        prompt_variation_number=1,
        prompt_variables={
            "python_exercice_statement": Variable(
                name="Python exercice statement",
                temperature=1,
                max_tokens=120,
                generation_number=10
            )
        },
        completion_variables={
            "python_code": Variable(
                name="Python code",
                temperature=0,
                max_tokens=256,
                generation_number=1
            )
        }
    )
    
    data = generator.generate_data(template=user_template, 
                         output_path="output.csv")

    print(data)

def anonymize_text(): 

    text_to_anonymize = """
        My name is Thomas, Call me at 0601010129 or email me at john.doe@example.com. 
        My SSN is 123-45-6789 and 4242 4242 8605 2607 is my credit card number. 
        Living in the best city in the world: Melbourne.
        New York & Co is a restaurant.
        It is 10 am.
        I have 10€ in my pocket. Oh my god.
        I have park my Tesla next to your house.
        My id is 0//1//2//2//2//2
    """

    completion_model = OpenAIModel(model_name=ModelName.GPT_35_TURBO_CHAT)

    anonymizer = Anonymizer(completion_model=completion_model)

    anonymized_text = anonymizer.anonymize(text=text_to_anonymize)
    
    print(anonymized_text)

def generate_variations_with_same_structure():

    structure_to_replicate = """
        My name is {first_name}, Call me at {phone_number} or email me at {email_address}. 
    """

    variation_model = OpenAIModel(model_name=ModelName.GPT_35_TURBO_CHAT)
    completion_model = OpenAIModel(model_name=ModelName.GPT_35_TURBO_CHAT)

    generator = DataGenerator(variation_model=variation_model, completion_model=completion_model)

    generator.generate_variation_with_same_structure(text=structure_to_replicate)

if __name__ == "__main__":

    generate_data_from_predefined_template()
    #generate_data_from_user_defined_template()
    #anonymize_text()
    #generate_variations_with_same_structure()

