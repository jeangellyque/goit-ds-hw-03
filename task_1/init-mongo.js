const catsDb = db.getSiblingDB("cats_db");

const cats = [
  {
    _id: ObjectId("6569853470e17dadb1d9d019"),
    name: "barsik",
    age: 3,
    features: ["ходить в капці", "дає себе гладити", "рудий"],
  },
  {
    _id: ObjectId("6569863470e17dadb1d9d01a"),
    name: "Lama",
    age: 2,
    features: ["ходить в лоток", "не дає себе гладити", "сірий"],
  },
  {
    _id: ObjectId("6569863470e17dadb1d9d01b"),
    name: "Liza",
    age: 4,
    features: ["ходить в лоток", "дає себе гладити", "білий"],
  },
  {
    _id: ObjectId("6569863470e17dadb1d9d01c"),
    name: "Boris",
    age: 12,
    features: ["ходить в лоток", "не дає себе гладити", "сірий"],
  },
  {
    _id: ObjectId("656988ac70e17dadb1d9d01e"),
    name: "Dariy",
    age: 10,
    features: ["ходить в лоток", "не дає себе гладити", "сірий"],
  },
  {
    _id: ObjectId("6569863470e17dadb1d9d01d"),
    name: "Murzik",
    age: 1,
    features: ["ходить в лоток", "дає себе гладити", "чорний"],
  },
];

cats.forEach((cat) => {
  catsDb.cats.updateOne(
    { name: cat.name },
    { $setOnInsert: cat },
    { upsert: true },
  );
});
