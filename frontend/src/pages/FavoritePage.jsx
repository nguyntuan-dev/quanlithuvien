import { useEffect, useState } from 'react'
import { yeuThichApi } from '../services/api'
import { Badge, Spinner, Empty } from '../components/UI'
import { BookOpen, Trash2 } from 'lucide-react'
import toast from 'react-hot-toast'

export default function FavoritePage() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)

  const load = async () => {
    setLoading(true)
    try {
      const { data } = await yeuThichApi.list()
      setItems(data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const handleRemove = async (ma) => {
    try {
      await yeuThichApi.remove(ma)
      toast.success('Đã xóa khỏi danh sách yêu thích')
      load()
    } catch (err) {
      toast.error('Không thể xóa')
    }
  }

  return (
    <div className="mx-auto max-w-6xl px-6 py-6">
      <div className="mb-5">
        <h1 className="text-lg font-bold tracking-tight">Sách yêu thích</h1>
        <p className="text-xs text-[#8c857b]">Danh sách các cuốn sách bạn đã lưu để xem sau</p>
      </div>

      {loading ? <Spinner /> : items.length === 0 ? <Empty message="Chưa có cuốn sách yêu thích nào" /> : (
        <div className="grid grid-cols-2 gap-x-4 gap-y-6 sm:gap-x-5 sm:gap-y-7 md:grid-cols-3 xl:grid-cols-4">
          {items.map(item => {
            const book = item.tai_lieu
            return (
              <article key={item.id} className="group relative">
                <div className="aspect-[3/4.25] relative overflow-hidden bg-surface-muted shadow-sm transition group-hover:-translate-y-0.5 group-hover:shadow-md">
                  {book.anh_bia ? (
                    <img src={book.anh_bia} alt={book.ten_tai_lieu} className="h-full w-full object-cover" />
                  ) : (
                    <div className="flex h-full w-full items-center justify-center text-ink-faint">
                      <BookOpen size={28} strokeWidth={1.25} />
                    </div>
                  )}
                  <button
                    type="button"
                    onClick={() => handleRemove(book.ma_tai_lieu)}
                    className="absolute right-2 top-2 rounded-full bg-white/90 p-1.5 text-danger shadow-md transition-all hover:bg-danger hover:text-white md:opacity-0 md:group-hover:opacity-100"
                    aria-label="Xóa khỏi yêu thích"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>

                <div className="mt-2.5 space-y-1">
                  <h3 className="line-clamp-2 text-[11px] font-semibold uppercase leading-snug tracking-wide text-[#1f1f1f]">
                    {book.ten_tai_lieu}
                  </h3>
                  <p className="truncate text-[10px] text-[#827c72]">{book.tac_gia?.ten_tac_gia || 'Ẩn danh'}</p>
                  <div className="flex flex-wrap items-center gap-1">
                    <Badge variant="blue" className="!px-1.5 !py-0 !text-[9px] !font-medium normal-case">
                      {book.the_loai?.ten_the_loai || 'Chưa phân loại'}
                    </Badge>
                    <Badge variant={book.so_luong > 0 ? 'green' : 'red'} className="!px-1.5 !py-0 !text-[9px] !font-medium">
                      {book.so_luong > 0 ? 'Còn sách' : 'Hết sách'}
                    </Badge>
                  </div>
                  <p className="font-mono text-[9px] text-[#aaa49a]">{book.ma_tai_lieu}</p>
                </div>
              </article>
            )
          })}
        </div>
      )}
    </div>
  )
}
