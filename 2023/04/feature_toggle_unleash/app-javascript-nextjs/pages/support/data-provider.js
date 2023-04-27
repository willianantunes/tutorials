import { faker } from "@faker-js/faker"

export function generateListOfProfiles(numberOfItems = 10) {
  const userList = []

  for (let i = 0; i < numberOfItems; i++) {
    const sexType = faker.name.sexType()
    const user = {
      id: faker.datatype.uuid(),
      username: faker.internet.userName(),
      name: faker.name.firstName(sexType),
      sex: sexType.name,
      address: faker.address.streetAddress(true),
      mail: faker.internet.email(),
      birthdate: faker.date.between("1950-01-01", "2003-12-31").toISOString().slice(0, 10),
    }
    userList.push(user)
  }

  return userList
}
