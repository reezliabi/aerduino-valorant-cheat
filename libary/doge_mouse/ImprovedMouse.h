#include <HID.h>
#include "MouseAPI.h"

class Mouse_ : public MouseAPI
{
public:
    Mouse_(void);

protected: 
    virtual inline void SendReport(void* data, int length) override;
};
extern Mouse_ Mouse;