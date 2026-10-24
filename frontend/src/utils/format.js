const numberFormat = new Intl.NumberFormat('id-ID')

export const fmt = (n) => numberFormat.format(n)
export const km = (n) => `${fmt(n)} km`
