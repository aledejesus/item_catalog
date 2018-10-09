-- Dump for testing purposes
-- NOTE: All descriptions were extracted from wikipedia

BEGIN;
-- Create admin app user
INSERT INTO app_user(google_id, name, email)
  VALUES (1, 'Admin', 'admin@admin.com');

-- Create test categories
INSERT INTO category(name, description) VALUES
  ('Kitchenware', 'Any tools, utensils, appliances, dishes, and cookware, that can be used in the process of food preparation, cooking or baking, or the serving of food. Kitchenware can also be used to hold or store food before or after preparation.'),
  ('Gardening', 'The practice of growing and cultivating plants as part of horticulture. In gardens, ornamental plants are often grown for their flowers, foliage, or overall appearance.'),
  ('Clothing', 'Clothing is a collective term for items worn on the body. Clothing can be made of textiles, animal skin, or other thin sheets of materials put together. The wearing of clothing is mostly restricted to human beings and is a feature of all human societies.');

-- Create test items
INSERT INTO item(category_id, app_user_id, quantity, name, description) VALUES
  (1, 1, 5, 'Spoon', 'A spoon is a utensil consisting of a small shallow bowl (also known as a head), oval or round, at the end of a handle. A type of cutlery, especially as part of a place setting, it is used primarily for serving.'),
  (1, 1, 23, 'Frying pan', 'A frying pan, frypan, or skillet is a flat-bottomed pan used for frying, searing, and browning foods. It is typically 200 to 300 mm (8 to 12 in) in diameter with relatively low sides that flare outwards, a long handle, and no lid.'),
  (1, 1, 8, 'Eggbeater', 'An eggbeater is a handheld device with a crank on the side geared to one or more beaters. The user grips the handle with one hand and operates the crank with the other, creating the rotary action.'),
  (3, 1, 10, 'Overall', 'An overall, also called overalls, bib-and-brace overalls, or dungarees, is a type of garment which is usually used as protective clothing when working. The garment is sometimes referred to as a "pair of overalls" by analogy with "pair of trousers".');
COMMIT;