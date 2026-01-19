import { api } from 'src/boot/axios'
import type { BookingCreate, BookingRead } from 'src/types/models'

export async function listBookings(): Promise<BookingRead[]> {
  const res = await api.get('/bookings')
  return res.data
}

export async function createBooking(payload: BookingCreate): Promise<BookingRead> {
  const res = await api.post('/bookings', payload)
  return res.data
}

export async function deleteBooking(id: number): Promise<void> {
  await api.delete(`/bookings/${id}`)
}
