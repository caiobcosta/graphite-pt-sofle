import Carbon
import Foundation
let want = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "com.apple.keylayout.Brazilian-ABNT2"
// list enabled layouts
let enabled = TISCreateInputSourceList(nil, false).takeRetainedValue() as! [TISInputSource]
for s in enabled {
    if let id = TISGetInputSourceProperty(s, kTISPropertyInputSourceID) { let v = Unmanaged<CFString>.fromOpaque(id).takeUnretainedValue() as String; if v.contains("keylayout") { print("enabled:", v) } }
}
let all = TISCreateInputSourceList([kTISPropertyInputSourceID as String: want] as CFDictionary, true).takeRetainedValue() as! [TISInputSource]
guard let src = all.first, let ptr = TISGetInputSourceProperty(src, kTISPropertyUnicodeKeyLayoutData) else { print("layout not found:", want); exit(1) }
let data = Unmanaged<CFData>.fromOpaque(ptr).takeUnretainedValue() as Data
let names: [(String, UInt16)] = [("`'",0x32),("1",0x12),("2",0x13),("3",0x14),("4",0x15),("5",0x17),("6",0x16),("7",0x1A),("8",0x1C),("9",0x19),("0",0x1D),("-",0x1B),("=",0x18),("[ (HID RBRC=´)",0x21),("] (HID BSLS)",0x1E),("\\ (HID NUHS)",0x2A),(";",0x29),("' (HID QUOT=~)",0x27),(",",0x2B),(".",0x2F),("/ (HID SLSH)",0x2C),("NUBS (ISO §)",0x0A),("INT1 (ABNT /?)",0x5E),("Q",0x0C),("W",0x0D),("E",0x0E),("R",0x0F),("T",0x11),("Y",0x10),("U",0x20),("I",0x22),("O",0x1F),("P",0x23),("A",0x00),("S",0x01),("D",0x02),("F",0x03),("G",0x05),("H",0x04),("J",0x26),("K",0x28),("L",0x25),("Z",0x06),("X",0x07),("C",0x08),("V",0x09),("B",0x0B),("N",0x2D),("M",0x2E)]
func tr(_ vk: UInt16, _ mods: UInt32) -> String {
    var dead: UInt32 = 0; var len = 0; var buf = [UniChar](repeating: 0, count: 8)
    data.withUnsafeBytes { raw in
        let p = raw.baseAddress!.assumingMemoryBound(to: UCKeyboardLayout.self)
        _ = UCKeyTranslate(p, vk, UInt16(kUCKeyActionDown), (mods >> 8) & 0xFF, UInt32(LMGetKbdType()), UInt32(kUCKeyTranslateNoDeadKeysMask), &dead, 8, &len, &buf)
    }
    return String(utf16CodeUnits: buf, count: len)
}
let opt = UInt32(optionKey), sh = UInt32(shiftKey)
print("layout:", want)
for (n, vk) in names {
    print(String(format: "%-16@ plain=%@  shift=%@  opt=%@  opt+shift=%@", n as NSString, tr(vk,0) as NSString, tr(vk,sh) as NSString, tr(vk,opt) as NSString, tr(vk,opt|sh) as NSString))
}
