from langchain.prompts import PromptTemplate
from llm.output_parser.enum_parser import location_output_parser

prompt = PromptTemplate(
    template="""
    {format_instructions}
    What is the location category for a given location detail? Select one of these without reason
       dining
       attractions
       outdoor activities
       entertainment
       accommodation
    If the location detail doesn't fit any categories, classify it as the following:
       etc
    
    location detail: Australia Dairy Company is a renowned \"cha chaan teng\" (traditional Hong Kong restaurant) in Jordan, Hong Kong. It specializes in steamed milk pudding, earning it a 3.5 out of 5 rating on Tripadvisor. Known for its silken smooth egg white & milk custard (hot) and egg custard (cold), the restaurant also offers a variety of other dishes, including scrambled eggs. Located at G/F, 47-49 Parkes Street in Jordan, Kowloon, Australia Dairy Company has a phone number of 2730 1356 for those wishing to make a reservation or inquire about their menu\n
    Answer: dining
    
    location detail: Richard Fortey's \"Dry Store Room No. 1\" offers an exclusive glimpse into London's Natural History Museum. The book delves into the hidden chambers and storerooms, showcasing the vast and diverse collection that lies beyond public view. Fortey leads readers through a narrative that celebrates the dedication of scientists, curators, and researchers who safeguard and study these specimens, revealing the untold stories behind the museum's treasures.\n
    Answer: attractions
    
    location detail: MidwayUSA.com offers a comprehensive selection of products for shooting, hunting, and outdoor activities, with its Nitro Express™ shipping service providing fast and affordable delivery. Additionally, the USS Midway Giftshop in San Diego caters to those seeking logo clothing, gift items, and Top Gun memorabilia. The newly renovated Cafe 41 and grab-and-go stop, Jet Express, provide delicious food and beverage options. In a separate context, MIDWAY shop is a lifestyle design brand that extends from the travelogue MIDWAY, featuring a curated collection of goods inspired by the travels of its founders. Its offshoot, PRESS THE BUTTON, is a coffee takeout shop that aims to tell stories through taste, linking people and experiences from their journeys. Midway also boasts a diverse range of local and national brands at its Midway Merchants, ensuring that visitors won't leave empty-handed.\n
    Answer: outdoor activities
    
    location detail: teamLab Borderless is a digital art museum in Tokyo that offers a unique and immersive experience. The museum is home to a variety of interactive artworks that are designed to blur the boundaries between art and technology. Visitors can explore different rooms filled with light sculptures, projections, and sound installations. The museum also features a number of interactive exhibits that allow visitors to create their own works of art. teamLab Borderless is a popular destination for both tourists and locals, and it is recommended to book tickets in advance to avoid long lines.\n
    Answer: entertainment
    
    location detail: The Slow is an immersive experience that encourages rest, mindfulness, and personal growth. It is located in a prime location with easy access to restaurants, beaches, and shops. The hotel's staff is friendly and helpful, and the overall vibe is positive and welcoming. It promotes a slow living philosophy, urging guests to slow down and savor the moment. It offers sustainable and ethical fashion options made with organic materials and shipped plastic-free. The Slow's pricing and sourcing are transparent, and it is committed to ethical production practices. The Slow offers a variety of experiences designed to enhance relaxation and personal growth, including guided meditations, yoga classes, and cooking demonstrations.\n
    Answer: accommodation
    
    location detail: {content}\n
    Answer:
    """,
    input_variables=["context"],
    partial_variables={"format_instructions": location_output_parser.get_format_instructions()},
)