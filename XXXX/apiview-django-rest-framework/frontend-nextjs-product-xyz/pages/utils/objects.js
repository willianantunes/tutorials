export const removeEmptyKeys = obj => {
  const newEntries = Object.entries(obj).filter(([_, value]) => {
    const nullish = value ?? null
    return nullish !== null
  })

  return Object.fromEntries(newEntries)
}
