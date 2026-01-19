import type { BookingStatus } from 'src/types/models'

export function statusBadgeColor(status: BookingStatus): string {
  switch (status) {
    case 'confirmed': return 'positive'
    case 'pending': return 'warning'
    case 'completed': return 'info'
    case 'cancelled': return 'negative'
    default: return 'grey'
  }
}
