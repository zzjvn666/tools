#include <reg52.h>

// 系统时钟与波特率配置
#define FOSC 11059200L    // 晶振频率 11.0592MHz
#define BAUD 9600         // 串口波特率 9600

// 引脚定义
sbit KEY_SEND   = P3^2;   // 发送按键
sbit KEY_LISTEN = P3^3;   // 接收/回发按键
sbit LED_SEND   = P1^1;   // 发送状态指示灯
sbit LED_LISTEN = P1^0;   // 接收状态指示灯

// 函数声明
void delay_ms(unsigned int ms);                // 毫秒延时
void UART_Init(void);                          // 串口初始化
void UART_SendByte(unsigned char dat);          // 串口单字节发送
void UART_SendPacket(unsigned char *ptr, unsigned char len); // 数据包发送
unsigned char UART_ReceiveByte(void);           // 串口单字节接收
unsigned char UART_ReceivePacket(unsigned char *buf, unsigned char maxlen); // 数据包接收
void Clear_RX_Buffer(void);                     // 清空接收缓冲区
bit Key_Read_Listen(void);                     // 接收按键读取（带消抖）

// 全局变量：接收缓冲区
unsigned char rx_buf[20];
unsigned char rx_len = 0;

/*********************************************************
函数名称：main
功能描述：主函数，按键控制串口发送/接收/回发
*********************************************************/
void main(void)
{
    bit is_listening = 0;    // 监听状态标志
    bit has_data = 0;        // 数据接收完成标志

    UART_Init();             // 串口初始化
    LED_SEND = 1;            // 指示灯初始熄灭
    LED_LISTEN = 1;

    while(1)
    {
        // ===================== 按键发送数据 =====================
        if(KEY_SEND == 0)
        {
            delay_ms(10);    // 消抖
            if(KEY_SEND == 0)
            {
                // 待发送原始数据
                unsigned char raw_data[] = {0x02,0x04,0x06,0x08,0x0A,0x0C};
                LED_SEND = 0;        // 发送灯亮
                UART_SendPacket(raw_data, 6); // 发送数据包
                LED_SEND = 1;        // 发送灯灭
                while(KEY_SEND == 0); // 等待按键松开
            }
        }

        // ===================== 按键接收+回发数据 =====================
        if(Key_Read_Listen())
        {
            if(!is_listening && !has_data)
            {
                // 进入监听状态
                is_listening = 1;
                LED_LISTEN = 0;      // 接收灯亮
                Clear_RX_Buffer();   // 清空串口缓存

                // 等待并接收数据包
                rx_len = UART_ReceivePacket(rx_buf, 20);

                // 接收完成
                has_data = 1;
            }
            else if(has_data)
            {
                // 将接收到的数据回发
                LED_LISTEN = 0;
                UART_SendPacket(rx_buf, rx_len);
                LED_LISTEN = 1;

                // 重置状态
                is_listening = 0;
                has_data = 0;
                rx_len = 0;
            }
            while(Key_Read_Listen()); // 等待按键松开
        }
    }
}

/*********************************************************
函数名称：Key_Read_Listen
功能描述：接收按键读取，带消抖
返回值：1=按下，0=未按下
*********************************************************/
bit Key_Read_Listen(void)
{
    if(KEY_LISTEN == 0)
    {
        delay_ms(10);
        return (KEY_LISTEN == 0) ? 1 : 0;
    }
    return 0;
}

/*********************************************************
函数名称：delay_ms
功能描述：软件毫秒延时（11.0592M 晶振）
*********************************************************/
void delay_ms(unsigned int ms)
{
    unsigned int i,j;
    for(i=0; i<ms; i++)
        for(j=0; j<120; j++);
}

/*********************************************************
函数名称：UART_Init
功能描述：串口初始化 9600 8N1，定时器1模式2
*********************************************************/
void UART_Init(void)
{
    TMOD &= 0x0F;   // 清空定时器1模式位
    TMOD |= 0x20;   // 定时器1 模式2（8位自动重装）
    PCON |= 0x80;   // SMOD=1，倍频
    TH1 = 256 - FOSC / 12 / 16 / BAUD; // 波特率重装值
    TL1 = TH1;
    TR1 = 1;        // 启动定时器1
    SCON = 0x50;    // 串口模式1，允许接收
}

/*********************************************************
函数名称：UART_SendByte
功能描述：串口单字节发送
*********************************************************/
void UART_SendByte(unsigned char dat)
{
    SBUF = dat;
    while(TI == 0); // 等待发送完成
    TI = 0;         // 清除发送标志
}

/*********************************************************
函数名称：UART_SendPacket
功能描述：串口数据包发送
格式：0xFF + 长度 + 数据 + 0xFE
*********************************************************/
void UART_SendPacket(unsigned char *ptr, unsigned char len)
{
    UART_SendByte(0xFF);       // 帧头
    UART_SendByte(len);        // 数据长度
    while(len--)               // 循环发送数据
    {
        UART_SendByte(*ptr++);
    }
    UART_SendByte(0xFE);       // 帧尾
}

/*********************************************************
函数名称：UART_ReceiveByte
功能描述：串口单字节接收（阻塞等待）
*********************************************************/
unsigned char UART_ReceiveByte(void)
{
    while(RI == 0); // 等待接收完成
    RI = 0;         // 清除接收标志
    return SBUF;
}

/*********************************************************
函数名称：UART_ReceivePacket
功能描述：按协议接收数据包（阻塞）
返回值：接收到的数据长度
*********************************************************/
unsigned char UART_ReceivePacket(unsigned char *buf, unsigned char maxlen)
{
    unsigned char len, i;
    unsigned char header;

    // 等待帧头 0xFF
    while(1)
    {
        header = UART_ReceiveByte();
        if(header == 0xFF)
            break;
    }

    len = UART_ReceiveByte(); // 获取数据长度
    if(len > maxlen)          // 防止越界
        len = maxlen;

    // 读取数据
    for(i=0; i<len; i++)
    {
        buf[i] = UART_ReceiveByte();
    }

    UART_ReceiveByte(); // 读取帧尾 0xFE（丢弃）
    return len;
}

/*********************************************************
函数名称：Clear_RX_Buffer
功能描述：清空串口硬件接收缓冲区
*********************************************************/
void Clear_RX_Buffer(void)
{
    unsigned char tmp;
    while(RI)
    {
        RI = 0;
        tmp = SBUF;
    }
}