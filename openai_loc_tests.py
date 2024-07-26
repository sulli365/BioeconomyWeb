import openai
import json

# Set up your OpenAI API key
openai.api_key = 'your-api-key-here'

def get_company_location(company_info):
    """
    Uses OpenAI's API to determine the location of a company from the provided information.

    Args:
    company_info (dict): A dictionary containing company name and associated information.

    Returns:
    dict: A JSON object with the company name as the key and the location as the value.
    """
    company_name = company_info.get('name')
    company_data = company_info.get('info', '')

    # Construct the prompt for the LLM
    prompt = f"""
    I have information about a company. Please determine the most specific location of the company from the information provided. If the location cannot be confidently determined, return "Location Unknown".

    Company Name: {company_name}
    Information: {company_data}

    The output should be in the format of a JSON object where the company name is the key and the location is the value.
    """

    # Call the OpenAI API to get the response
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0,
        top_p=1
    )

    # Extract and format the result
    result = response.choices[0].text.strip()

    try:
        # Try to parse the result as JSON
        location_info = json.loads(result)
        # Ensure the result is a dictionary with a single entry
        if isinstance(location_info, dict) and len(location_info) == 1 and company_name in location_info:
            return location_info
    except json.JSONDecodeError:
        pass

    # If parsing fails or the format is incorrect, return "Location Unknown"
    return {company_name: "Location Unknown"}

# Example usage
company_info = {
    'name': 'BioTech Innovations',
    'info': 'BioTech Innovations specializes in advanced bioengineering solutions. Their headquarters are located in Boston, Massachusetts.'
}

location = get_company_location(company_info)
print(json.dumps(location, indent=2))
