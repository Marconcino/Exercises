export type BookingStatus = 'confirmed' | 'pending' | 'completed' | 'cancelled'

export interface TableRead {
  id: number
  table_number: number
  max_capacity: number
}

export interface ClientRead {
  id: number
  name: string
  phone: string
  email: string
}

export interface BookingRead {
  id: number
  client_id: number
  table_id: number
  reservation_date: string   // "YYYY-MM-DD"
  day_of_week: string        // or a stricter union later
  reservation_time: string   // "HH:MM:SS" (or "HH:MM")
  guest_count: number
  status: BookingStatus
  created_at: string
}

export interface BookingCreate {
  client_id: number
  table_id: number
  reservation_date: string
  reservation_time: string
  guest_count: number
  status?: BookingStatus
}
