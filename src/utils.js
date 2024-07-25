let toastID = 0
export const toastBuffer = ref([])
export function toast(toast) {
    toastID += 1
    toast.id = toastID
    toastBuffer.value.push(toast)
}
export function removeToast(id) {
    toastBuffer.value = toastBuffer.value.filter((toast) => toast.id != id)
}
export function ajaxFeedback(response) {
    toast({
        variant: response.success ? 'success' : 'danger',
        message: String(response.message),
        title: response.title,
    })
}